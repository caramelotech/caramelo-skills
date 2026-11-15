---
name: application-text
description: Gera o texto curto e personalizado para o campo de candidatura de plataformas de recrutamento (Gupy, por padrão com limite de 1500 caracteres, ou outro limite informado), com base na descrição da vaga (texto ou URL) e na trajetória profissional da pessoa. Antes de escrever, roda a preparação da skill interview-prep, então a nota de candidatura sai completa - dados da vaga, preparação de entrevista e texto da candidatura juntos. No primeiro uso coleta onde está a trajetória (arquivo, currículo, LinkedIn ou outro link, ou ajuda a criá-la se a pessoa não tiver), onde salvar e o idioma, e guarda no perfil de carreira compartilhado; depois só a vaga é necessária. Use quando a pessoa pedir texto para candidatura no Gupy ou em outro formulário de vaga com limite de caracteres.
allowed-tools:
  - Read(~/.claude/plugins/**/caramelo-skills/**)
  - Read(~/.claude/career/profile.json)
  - Edit(~/.claude/career/profile.json)
  - Skill
  - AskUserQuestion
---

# Texto de candidatura

Gera o texto curto para o campo de candidatura de plataformas de recrutamento, alinhado à vaga e à trajetória profissional. O padrão é o campo do Gupy (até 1500 caracteres), mas o limite pode ser trocado para outros formulários.

Diferente da `cover-letter` (carta longa, com saudação e despedida, para e-mail ou anexo) e de rodar só a `interview-prep` (que organiza os dados e prepara a entrevista, mas não escreve texto de candidatura), esta skill faz as duas coisas: roda a preparação e escreve o texto.

## Parâmetros

| Parâmetro          | Flag           | Obrigatório | O que é                                                                                         |
| ------------------ | -------------- | ----------- | ----------------------------------------------------------------------------------------------- |
| `<vaga>`           | `--vaga`       | Sim         | Descrição da vaga: texto colado, caminho de arquivo ou URL                                      |
| `[empresa]`        | `--empresa`    | Não         | Nome da empresa. Se não vier, é extraído da vaga                                                |
| `[limite]`         | `--limite`     | Não         | Limite de caracteres do campo. Padrão: `1500` (Gupy)                                            |
| `[foco]`           | `--foco`       | Não         | Texto livre: o que enfatizar, tom, pergunta específica do formulário que o texto deve responder |
| `--sem-preparacao` | -              | Não         | Pula a `interview-prep` e escreve só o texto (útil para formulários rápidos)                    |
| `[trajetoria]`     | `--trajetoria` | Não         | Caminho da trajetória. Sobrescreve o perfil só nesta chamada                                    |
| `[output]`         | `--output`     | Não         | Pasta da nota. Sobrescreve o perfil só nesta chamada                                            |
| `[idioma]`         | `--idioma`     | Não         | Idioma do texto. Sobrescreve o perfil só nesta chamada                                          |
| `--reconfigurar`   | -              | Não         | Refaz a configuração inicial do perfil                                                          |

Se a skill for chamada sem a vaga, peça só a vaga em uma mensagem de chat e aguarde.

## 1. Perfil

Leia e siga `../../shared/profile.md` (caminho relativo à pasta desta skill). Esta skill usa os campos `name`, `careerSource`, `extraSources`, `outputFolder`, `language` e `noteStyle`, e não tem perguntas próprias de configuração.

Se o arquivo compartilhado não puder ser lido, use `~/.claude/career/profile.json` diretamente e pergunte só a trajetória e a pasta de destino que faltarem.

## 2. Organizar os dados e preparar a entrevista

Exceto com `--sem-preparacao`, invoque a skill `interview-prep` da mesma categoria, repassando a vaga e as flags recebidas (`--empresa`, `--trajetoria`, `--output`, `--idioma`):

```
Skill({ skill: "career:interview-prep", args: "<vaga> [flags]" })
```

Se a skill não estiver disponível com o prefixo `career:`, tente `interview-prep`. Se não estiver disponível de nenhuma forma, faça a análise da vaga (tecnologias, domínio, nível, responsabilidades, diferenciais) internamente e avise na resposta final que a nota saiu sem a preparação de entrevista.

A `interview-prep` cria ou atualiza a nota `Candidatura <Empresa>.md` em `outputFolder`. Não repita a análise: reaproveite o que ela devolveu e a nota que ela gravou.

Com `--sem-preparacao`, receba a vaga seguindo "Receber a vaga" do perfil compartilhado e faça a análise internamente, sem gravar a preparação.

## 3. Ler a trajetória

Siga "Ler a trajetória" do perfil compartilhado, para ter o mesmo contexto da preparação na hora de escrever.

## 4. Escrever o texto

Escreva no idioma do perfil (ou de `--idioma`; com `vaga`, no idioma da descrição), direto e pessoal, em texto puro: sem bullet points, sem negrito, sem títulos, sem saudação e sem assinatura (as plataformas já mostram o nome do perfil). O texto deve:

- Abrir com a experiência mais relevante para a vaga.
- Citar as tecnologias da vaga que a trajetória comprova, usando os termos exatos da descrição.
- Ancorar o texto na experiência atual, como ponto de partida.
- Destacar uma experiência passada quando ela atender diretamente a um requisito específico da vaga (mesma tecnologia, mesmo domínio, mesmo tipo de sistema). Ela vem da trajetória, nunca de suposição.
- Incluir o diferencial de carreira quando a vaga valorizar o que ele demonstra.
- Fechar com motivação genuína para aquela empresa ou produto, não genérica.
- Ser neutro quanto ao gênero ao falar da própria pessoa, quando possível ("minha trajetória", "atuo como").
- Se `--foco` trouxer uma pergunta do formulário (por exemplo, "Por que você quer trabalhar aqui?"), responder a ela em vez de seguir a estrutura acima à risca.

### Limite de caracteres

O texto final deve ter **no máximo `limite` caracteres** (padrão 1500), contando espaços, pontuação e quebras de linha.

Conte com precisão em vez de estimar. Conte **caracteres**, não bytes (`wc -c` conta bytes e superestima textos com acentos). Passe o texto pela entrada padrão com heredoc de delimitador entre aspas simples, sem arquivo temporário e sem interpolação do shell:

```bash
python -I -c "import sys; print(len(sys.stdin.buffer.read().decode('utf-8').rstrip('\r\n')))" <<'TXT'
<texto final>
TXT
```

Se `python` não existir, use `LC_ALL=C.UTF-8 wc -m` com o mesmo heredoc e desconte a quebra de linha final. O comando pede permissão na primeira vez; não troque por outro para evitar o pedido.

Se passar do limite, corte passagens genéricas ou detalhes menos relevantes para a vaga. Nunca corte as menções às tecnologias exigidas que a trajetória comprova. Conte de novo depois de cada corte.

## 5. Apresentar o resultado

Exiba:

1. **O texto da candidatura**, pronto para colar.
2. **Contagem:** `XXX / <limite>`.
3. **Tecnologias da vaga cobertas:** lista curta do que foi mencionado.
4. **Requisitos não cobertos:** o que a vaga pede e a trajetória não comprova, e por isso ficou de fora.

Pergunte se a pessoa quer ajustes (tom, foco, ênfase em alguma tecnologia, corte de algum trecho).

## 6. Atualizar a nota de candidatura

A nota `Candidatura <Empresa>.md` em `outputFolder` já existe (criada no passo 2). Não a recrie: só adicione ou atualize a seção abaixo.

```markdown
## Texto da Candidatura

<texto final, em parágrafos, sem blockquote>

**Caracteres:** XXX / <limite>
```

Com `--sem-preparacao` e sem nota existente, crie a nota com o frontmatter e a seção "Sobre a Vaga" do modelo da `interview-prep` e esta seção, sem a preparação de entrevista.

Se a pessoa pedir ajustes depois, atualize só essa seção com a versão final. Na primeira execução, diga também onde o perfil foi salvo e como mudá-lo.

## Restrições

- Nome, empregadores, tecnologias e diferenciais vêm sempre da trajetória informada, nunca de suposições.
- Evitar formulações genéricas como "profissional apaixonado" ou "sou alguém que ama tecnologia".
- Não incluir saudação nem assinatura.
- Não ultrapassar o limite de caracteres em hipótese alguma.
- Tom profissional, mas humano: não soar como currículo em lista.
- Não usar travessão (—); usar hífen (-).
- Não usar `---` como separador no corpo da nota (apenas no frontmatter).
- Não enviar a candidatura, preencher formulários nem publicar nada em nome da pessoa.
- Não fazer `git commit` nem `git push`.

## Exemplo

**Input:**

```
/career:application-text https://empresa.gupy.io/jobs/123456
```

**Output esperado:**

```
<texto da candidatura, em 2 a 4 parágrafos curtos>

Contagem: 1.412 / 1500
Tecnologias cobertas: Java, Spring Boot, PostgreSQL, AWS
Não cobertos: Kafka (não aparece na trajetória)
Nota atualizada: Documents/Candidaturas/Candidatura Acme.md

Quer ajustar o tom, o foco ou cortar algum trecho?
```

**Outro formulário, com limite diferente:**

```
/career:application-text --limite 1000 --sem-preparacao --foco "Por que você quer trabalhar na Acme?" "<descrição da vaga>"
```
