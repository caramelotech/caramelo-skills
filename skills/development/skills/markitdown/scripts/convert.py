# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "markitdown[pdf,docx,pptx,xlsx,xls,outlook]==0.1.9",
#     "pypdfium2==5.15.2",
#     "pytesseract==0.3.13",
# ]
# ///
"""Convert local documents to Markdown with MarkItDown, fully offline.

Security guarantees enforced by this wrapper (not by the caller):

- Only existing local files are accepted: URLs and URI schemes are rejected.
- Only an allowlist of extensions is converted; audio/video are refused because
  MarkItDown's transcription relies on an online service.
- Network access is disabled inside this process (socket and DNS are patched
  before MarkItDown is imported), so no converter can reach the internet.
- Plugins, Azure Document Intelligence, Content Understanding and LLM clients
  are never enabled.
- File size, ZIP-based containers (docx, pptx, xlsx, epub, zip) and OCR page
  count are bounded to mitigate decompression bombs and resource exhaustion.
- Existing output files are never overwritten unless --force is given.

Exit codes: 0 ok, 2 invalid input, 3 security limit hit, 4 conversion failed,
5 environment problem (missing dependency or OCR engine).
"""

from __future__ import annotations

import argparse
import io
import os
import re
import shutil
import socket
import sys
import zipfile
from pathlib import Path

EXIT_OK = 0
EXIT_INVALID = 2
EXIT_LIMIT = 3
EXIT_CONVERSION = 4
EXIT_ENV = 5

ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".msg",
    ".html", ".htm", ".csv", ".json", ".xml", ".txt", ".md",
    ".epub", ".ipynb", ".zip",
    ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp",
}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
ZIP_BASED_EXTENSIONS = {".docx", ".pptx", ".xlsx", ".epub", ".zip"}
REFUSED_EXTENSIONS = {
    ".mp3", ".wav", ".m4a", ".mp4", ".ogg", ".flac", ".aac", ".webm", ".mov",
}

DEFAULT_MAX_SIZE_MB = 100
DEFAULT_MAX_UNCOMPRESSED_MB = 1024
DEFAULT_MAX_ZIP_ENTRIES = 10_000
MAX_COMPRESSION_RATIO = 200
MAX_ZIP_DEPTH = 2
DEFAULT_MAX_OCR_PAGES = 200
OCR_DPI = 300
# Average of non-whitespace characters per page below which a PDF is treated
# as scanned (image-only) and OCR is attempted in "auto" mode.
SCANNED_CHARS_PER_PAGE = 30

URI_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://|^(data|file|javascript):", re.I)
WINDOWS_TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")


class SkillError(Exception):
    def __init__(self, message: str, code: int) -> None:
        super().__init__(message)
        self.code = code


def block_network() -> None:
    """Make any socket connection or DNS lookup in this process fail."""

    def refuse(*_args, **_kwargs):
        raise OSError("network access is disabled by the markitdown skill")

    socket.socket.connect = refuse  # type: ignore[method-assign]
    socket.socket.connect_ex = refuse  # type: ignore[method-assign]
    socket.socket.sendto = refuse  # type: ignore[method-assign]
    socket.create_connection = refuse  # type: ignore[assignment]
    socket.getaddrinfo = refuse  # type: ignore[assignment]
    socket.gethostbyname = refuse  # type: ignore[assignment]
    socket.gethostbyname_ex = refuse  # type: ignore[assignment]


def validate_input(raw: str, max_size_mb: int) -> Path:
    if URI_SCHEME.match(raw.strip()):
        raise SkillError(
            "URLs and URI schemes are not accepted: download the file yourself "
            "and pass a local path", EXIT_INVALID)
    path = Path(raw).expanduser()
    if not path.exists():
        raise SkillError(f"file not found: {path}", EXIT_INVALID)
    path = path.resolve(strict=True)
    if not path.is_file():
        raise SkillError(f"not a regular file: {path}", EXIT_INVALID)
    ext = path.suffix.lower()
    if ext in REFUSED_EXTENSIONS:
        raise SkillError(
            f"{ext} is refused: MarkItDown transcribes audio with an online "
            "service, which breaks the local-only guarantee", EXIT_INVALID)
    if ext not in ALLOWED_EXTENSIONS:
        raise SkillError(
            f"extension {ext or '(none)'} is not in the allowlist: "
            + ", ".join(sorted(ALLOWED_EXTENSIONS)), EXIT_INVALID)
    size = path.stat().st_size
    if size > max_size_mb * 1024 * 1024:
        raise SkillError(
            f"file is {size / 1024 / 1024:.1f} MB, above the {max_size_mb} MB "
            "limit (raise it with --max-size-mb if you trust the file)", EXIT_LIMIT)
    return path


def inspect_zip(source, max_total: int, max_entries: int, depth: int = 0) -> int:
    """Check a ZIP container (and nested ZIP-based entries) against bomb limits.

    Returns the declared uncompressed size, raising SkillError on violations.
    """
    try:
        archive = zipfile.ZipFile(source)
    except zipfile.BadZipFile as exc:
        raise SkillError(f"invalid ZIP container: {exc}", EXIT_INVALID) from exc
    with archive:
        infos = archive.infolist()
        if len(infos) > max_entries:
            raise SkillError(
                f"container has {len(infos)} entries, above the {max_entries} limit",
                EXIT_LIMIT)
        total = 0
        for info in infos:
            total += info.file_size
            if total > max_total:
                raise SkillError(
                    "declared uncompressed size is above the "
                    f"{max_total // 1024 // 1024} MB limit (possible ZIP bomb)",
                    EXIT_LIMIT)
            if info.compress_size and info.file_size > 1024 * 1024:
                ratio = info.file_size / info.compress_size
                if ratio > MAX_COMPRESSION_RATIO:
                    raise SkillError(
                        f"entry {info.filename!r} has compression ratio {ratio:.0f}:1 "
                        "(possible ZIP bomb)", EXIT_LIMIT)
            if Path(info.filename).suffix.lower() in ZIP_BASED_EXTENSIONS:
                if depth + 1 > MAX_ZIP_DEPTH:
                    raise SkillError(
                        f"nested archives deeper than {MAX_ZIP_DEPTH} levels",
                        EXIT_LIMIT)
                with archive.open(info) as inner:
                    data = inner.read(max_total + 1)
                if len(data) > max_total:
                    raise SkillError("nested entry exceeds size limit", EXIT_LIMIT)
                total += inspect_zip(io.BytesIO(data), max_total - total,
                                     max_entries, depth + 1)
        return total


def find_tesseract() -> str | None:
    env = os.environ.get("TESSERACT_CMD")
    if env and Path(env).is_file():
        return env
    found = shutil.which("tesseract")
    if found:
        return found
    if WINDOWS_TESSERACT.is_file():
        return str(WINDOWS_TESSERACT)
    return None


def resolve_ocr_lang(requested: str | None, tesseract_cmd: str) -> str:
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    installed = set(pytesseract.get_languages(config=""))
    if requested:
        missing = [lang for lang in requested.split("+") if lang not in installed]
        if missing:
            raise SkillError(
                f"OCR language(s) not installed in Tesseract: {', '.join(missing)}",
                EXIT_ENV)
        return requested
    preferred = [lang for lang in ("por", "eng") if lang in installed]
    if not preferred:
        raise SkillError(
            "Tesseract has neither 'por' nor 'eng' installed; pass --ocr-lang",
            EXIT_ENV)
    return "+".join(preferred)


def ocr_images(images, lang: str) -> str:
    import pytesseract

    parts = []
    for index, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image, lang=lang).strip()
        parts.append(f"<!-- page {index} (OCR) -->\n\n{text}")
    return "\n\n".join(parts)


def ocr_pdf(path: Path, lang: str, max_pages: int) -> tuple[str, int]:
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(path))
    try:
        page_count = len(pdf)
        if page_count > max_pages:
            raise SkillError(
                f"PDF has {page_count} pages, above the OCR limit of {max_pages} "
                "(raise it with --max-ocr-pages)", EXIT_LIMIT)

        def pages():
            for index in range(page_count):
                page = pdf[index]
                try:
                    yield page.render(scale=OCR_DPI / 72).to_pil()
                finally:
                    page.close()

        return ocr_images(pages(), lang), page_count
    finally:
        pdf.close()


def pdf_page_count(path: Path) -> int:
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(path))
    try:
        return len(pdf)
    finally:
        pdf.close()


def check_environment() -> int:
    """Report what is available; used once to warm the uv cache."""
    import markitdown

    print(f"markitdown {markitdown.__version__}: ok")
    tesseract = find_tesseract()
    if not tesseract:
        print("tesseract: not found (OCR unavailable; install it to read scanned "
              "PDFs and images)")
        return EXIT_OK
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = tesseract
    langs = sorted(pytesseract.get_languages(config=""))
    shown = [lang for lang in langs if lang in ("por", "eng")] or langs[:5]
    print(f"tesseract {pytesseract.get_tesseract_version()}: {tesseract}")
    print(f"tesseract languages (por/eng): {', '.join(shown) or 'none'}")
    return EXIT_OK


def convert(args: argparse.Namespace) -> int:
    path = validate_input(args.input, args.max_size_mb)
    ext = path.suffix.lower()

    if ext in ZIP_BASED_EXTENSIONS:
        inspect_zip(path, args.max_uncompressed_mb * 1024 * 1024,
                    DEFAULT_MAX_ZIP_ENTRIES)

    output: Path | None = None
    if not args.stdout:
        output = (Path(args.output).expanduser() if args.output
                  else path.with_suffix(".md"))
        output = output.resolve()
        if output == path:
            raise SkillError("output would overwrite the input file", EXIT_INVALID)
        if output.exists() and not args.force:
            raise SkillError(
                f"output already exists: {output} (use --force to overwrite)",
                EXIT_INVALID)

    from markitdown import MarkItDown

    # Only built-in converters; never plugins, docintel, CU or LLM clients.
    md = MarkItDown(enable_builtins=True, enable_plugins=False)
    try:
        result = md.convert_local(str(path))
        text = result.markdown or ""
    except Exception as exc:  # noqa: BLE001 - surface any converter failure
        text = ""
        conversion_error = exc
    else:
        conversion_error = None

    ocr_used = False
    notes: list[str] = []
    wants_ocr = args.ocr != "never" and (ext == ".pdf" or ext in IMAGE_EXTENSIONS)
    if wants_ocr:
        visible = len(re.sub(r"\s", "", text))
        if ext == ".pdf":
            pages = max(pdf_page_count(path), 1)
            scanned = visible / pages < SCANNED_CHARS_PER_PAGE
        else:
            scanned = True  # images carry no text layer
        if args.ocr == "always" or scanned:
            tesseract = find_tesseract()
            if not tesseract:
                notes.append("OCR skipped: Tesseract not found (set TESSERACT_CMD "
                             "or install it)")
            else:
                lang = resolve_ocr_lang(args.ocr_lang, tesseract)
                if ext == ".pdf":
                    ocr_text, _ = ocr_pdf(path, lang, args.max_ocr_pages)
                else:
                    from PIL import Image

                    with Image.open(path) as image:
                        ocr_text = ocr_images([image], lang)
                text = (text.rstrip() + "\n\n" if text.strip() and ext in
                        IMAGE_EXTENSIONS else "") + ocr_text
                ocr_used = True
                notes.append(f"OCR applied with Tesseract ({lang})")

    if conversion_error is not None and not ocr_used:
        raise SkillError(f"conversion failed: {conversion_error}", EXIT_CONVERSION)
    if not text.strip():
        notes.append("no text extracted (scanned document without OCR, "
                     "protected file, or empty content)")

    if args.stdout:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    else:
        assert output is not None
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8", newline="\n")
        print(f"output: {output}", file=sys.stderr)

    print(f"chars: {len(text)}", file=sys.stderr)
    print(f"ocr: {'yes' if ocr_used else 'no'}", file=sys.stderr)
    for note in notes:
        print(f"note: {note}", file=sys.stderr)
    return EXIT_OK


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a local document to Markdown with MarkItDown, offline.")
    parser.add_argument("input", nargs="?", help="local file to convert")
    parser.add_argument("-o", "--output", help="output .md path "
                        "(default: next to the input, same name)")
    parser.add_argument("--stdout", action="store_true",
                        help="print Markdown to stdout instead of writing a file")
    parser.add_argument("--force", action="store_true",
                        help="overwrite the output file if it exists")
    parser.add_argument("--ocr", choices=("auto", "always", "never"), default="auto",
                        help="OCR scanned PDFs and images with local Tesseract")
    parser.add_argument("--ocr-lang", help="Tesseract languages, e.g. por+eng")
    parser.add_argument("--max-size-mb", type=int, default=DEFAULT_MAX_SIZE_MB)
    parser.add_argument("--max-uncompressed-mb", type=int,
                        default=DEFAULT_MAX_UNCOMPRESSED_MB)
    parser.add_argument("--max-ocr-pages", type=int, default=DEFAULT_MAX_OCR_PAGES)
    parser.add_argument("--check", action="store_true",
                        help="check dependencies and OCR engine, then exit")
    args = parser.parse_args(argv)
    if not args.check and not args.input:
        parser.error("input is required unless --check is given")
    if args.stdout and args.output:
        parser.error("--stdout and --output are mutually exclusive")
    return args


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parse_args(argv)
    block_network()
    try:
        return check_environment() if args.check else convert(args)
    except SkillError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exc.code
    except ImportError as exc:
        print(f"error: missing dependency ({exc}); run the script with "
              "`uv run --script` so the pinned dependencies are installed",
              file=sys.stderr)
        return EXIT_ENV


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
