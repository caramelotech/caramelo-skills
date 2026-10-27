# Changelog

Todas as mudanças notáveis deste repositório são documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

Cada categoria em `skills/` tem sua própria versão, declarada em `.claude-plugin/plugin.json`. A versão listada aqui no topo é a do marketplace (`.claude-plugin/marketplace.json`) como um todo. Como o repositório ainda não teve nenhuma versão publicada, todo o trabalho até aqui faz parte do primeiro lançamento (1.0.0) - a partir do próximo commit e push, mudanças estruturais passam a exigir um novo bump de versão.

## [Não lançado]

### Adicionado

- Skill `bruno-collection` na categoria `development` (1.4.0): cria e mantém collections do Bruno a partir do código do projeto, de uma spec OpenAPI ou de uma lista de endpoints. Gera os arquivos em YAML (OpenCollection) em `.bruno/` na raiz do repositório, organiza pastas por recurso, ambientes e variáveis por escopo, configura a autenticação com credenciais em `.env` ignorado pelo git (ou variáveis secretas do Bruno) e tokens em variáveis de runtime, e documenta as regras de cada endpoint (validações, permissões, respostas, efeitos colaterais). Novas preferências em `skills.bruno-collection`: `secretStrategy`, `environments`, e por repositório `collectionPath` e `format`.

### Alterado

- Repositório e marketplace renomeados de `caramelo-kit` para `caramelo-skills`. Quem já tinha o marketplace instalado deve removê-lo (`/plugin marketplace remove caramelo-kit`), adicioná-lo de novo (`/plugin marketplace add caramelotech/caramelo-skills`) e reinstalar as categorias como `<categoria>@caramelo-skills`.

## [2.0.0] - 2026-10-10

### Adicionado

- Preferências persistentes na categoria `development` (`~/.claude/development/preferences.json`, procedimento em `skills/development/shared/preferences.md`), com modo de autonomia global (`assistido` ou `autonomo`), preferências por skill e por repositório, e reconfiguração por `--reconfigurar`, `--preferencias` ou pedido em linguagem natural. No modo `autonomo`, as skills executam sem esperar resposta e relatam ao final, sempre parando antes de ações irreversíveis.
  - `commit-message`: política para branches protegidas (perguntar, commitar direto ou criar branch nova), confirmação do plano, push (`never`, `ask` ou `auto`), `Signed-off-by` padrão e idioma das mensagens. Novas flags `--no-sign`, `--push` e `--no-push`.
  - `code-review` e `owasp-check`: saída no chat ou em arquivo, severidade mínima e correções (sugerir, perguntar ou aplicar). A `code-review` pode incluir a `owasp-check` sempre.
  - `unit-test-generator`: escrever os testes no repositório ou só no chat, rodar os testes, padrão de nomes, e framework e pasta de testes detectados e lembrados por repositório.
  - `technical-cofounder`: preferências movidas para o arquivo comum da categoria e nível de check-ins (`stage`, `phase` ou `minimal`).

### Alterado

- Skills `unit-test-generator` e `owasp-check` movidas para a categoria `development` (1.3.0), em `skills/development/skills/`. Passam a ser chamadas como `development:unit-test-generator` e `development:owasp-check`.
- Agents `code-reviewer` e `test-generator`, `AGENTS.md`, `README.md` e `CONTRIBUTING.md` atualizados para os novos caminhos.

### Removido

- Categorias `testing` e `security`, e os respectivos registros no marketplace. Quem instalou `testing@caramelo-kit` ou `security@caramelo-kit` deve desinstalá-las e instalar (ou atualizar) `development@caramelo-kit`.

## [career 1.1.0] - 2026-10-10

### Adicionado

- Skill `linkedin-review`: avalia o perfil do LinkedIn contra um objetivo de carreira e gera um relatório com sugestões e racional por seção (título, Sobre, Experiência, palavras-chave, teste do recrutador, Destaques e DMs). Guarda o link do perfil, a cópia do conteúdo e o objetivo de carreira (setor, cargo-alvo e empresas-alvo) no perfil compartilhado, usa a trajetória profissional para completar métricas sem inventar e compara cada rodada com a avaliação anterior.

## [development 1.2.0] - 2026-10-10

### Adicionado

- Skill `technical-cofounder`: conduz a pessoa da ideia até um produto funcional em 5 fases com portões de aprovação. Guarda nas preferências de desenvolvimento (`~/.claude/development/preferences.json`) o nível técnico (que calibra a linguagem da conversa), a pasta de projetos, a stack e a hospedagem preferidas e o registro de projetos em andamento, para retomar um projeto de onde parou.

## [1.1.0] - 2026-10-10

### Adicionado

- Categoria `study` (1.0.0), registrada no marketplace, com a skill `lecture-notes`: transforma uma aula (transcrição, notas e/ou título) em uma nota de estudo didática para revisão, com referencial teórico pesquisado em fontes confiáveis. Pergunta o destino a cada chamada e guarda cursos e pastas em `~/.claude/lecture-notes/courses.json` para oferecê-los nas próximas.
- Categoria `career` (1.0.0), registrada no marketplace, com três skills que compartilham um perfil de carreira (`~/.claude/career/profile.json`, procedimento em `skills/career/shared/profile.md`): no primeiro uso coletam trajetória, destino, idioma e formato; nas chamadas seguintes só a vaga é necessária. Quando a pessoa não informa a trajetória profissional, as skills explicam por que ela é necessária e ajudam a obtê-la: a partir de arquivo, currículo em PDF ou `.docx`, LinkedIn (via export em PDF ou texto colado, sem login), portfólio e GitHub, ou por criação guiada, consolidando tudo em `Trajetoria Profissional.md`.
  - `cover-letter`: carta de apresentação completa para e-mail, LinkedIn ou anexo, em nota, `.docx`, PDF ou só no chat.
  - `interview-prep`: nota de candidatura com análise da vaga e preparação para entrevista (perguntas prováveis, pontos fortes, lacunas e perguntas para a pessoa entrevistadora).
  - `application-text`: texto curto para o campo de candidatura (Gupy, 1500 caracteres por padrão, ou outro limite), rodando a `interview-prep` antes e contando caracteres com precisão.

## [development 1.1.0] - 2026-10-10

### Adicionado

- Seção "Princípios de execução" nas skills `code-review` e `commit-message`, com diretrizes comportamentais para reduzir erros comuns de assistentes de IA (presunção de contexto, abstrações especulativas, mistura de bug com preferência de estilo, falta de critério verificável), adaptadas ao escopo de cada skill.

## [1.0.0] - 2026-10-10

### Adicionado

- Estrutura inicial do repositório: skills organizadas por categoria em `skills/<categoria>/skills/<nome>/SKILL.md`, cada categoria como plugin independente do Claude Code (`development`, `writing`, `testing`, `devops`, `security`, `design`), com `.claude-plugin/plugin.json` próprio (nome, versão, descrição, autor, licença, keywords).
- Skills: `code-review` e `commit-message` (`development`); `unit-test-generator` (`testing`); `text-writer` e `text-humanizer` (`writing`); `dockerfile-review` (`devops`); `owasp-check` (`security`); `apply-design-system` (`design`), com o design system do Notion catalogado como primeira referência em `references/notion.md`.
- Agents: `code-reviewer`, `test-generator`, `doc-writer`.
- `templates/` para criar novas skills, agents e integrações externas.
- `.claude-plugin/marketplace.json` registrando as categorias como plugins instaláveis via `/plugin marketplace add` e `/plugin install <categoria>@caramelo-kit`.
- `.github/CONTRIBUTING.md` com o guia de contribuição (skills, categorias, agents e integrações externas).
- Este `CHANGELOG.md`.
- Licença MIT.
