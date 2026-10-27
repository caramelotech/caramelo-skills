# Caramelo Skills 🐶

Repositório de skills, agents e plugins para desenvolvimento de software. As skills são organizadas em **categorias** e distribuídas como plugins instaláveis via marketplace do Claude Code.

## Estrutura

O repositório tem quatro áreas principais: `skills/` (skills agrupadas por categoria, cada categoria um plugin independente do Claude Code), `agents/` (orquestradores que combinam múltiplas skills), `plugins/` (integrações com ferramentas externas, não confundir com os plugins do Claude Code) e `templates/` (ponto de partida para cada um desses itens). O registro do marketplace fica em `.claude-plugin/marketplace.json` e o histórico de versões em `CHANGELOG.md`. Detalhes de como criar cada item estão no [guia de contribuição](.github/CONTRIBUTING.md).

## Categorias disponíveis

| Categoria                           | Descrição                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------- |
| [`development`](skills/development) | Qualidade, revisão, segurança, testes, commits, collections do Bruno e MVPs |
| [`writing`](skills/writing)         | Criação de textos, humanização e documentação                               |
| [`devops`](skills/devops)           | Infraestrutura e containerização                                            |
| [`design`](skills/design)           | Aplicação de design systems em apresentações e sites                        |
| [`study`](skills/study)             | Estudos e produtividade: notas de aula para revisão                         |
| [`career`](skills/career)           | Carreira: cartas, textos de candidatura e entrevistas                       |

## Como instalar

### Via marketplace do Claude Code (recomendado)

1. Registre este repositório como marketplace. De dentro de uma sessão do Claude Code:

   ```
   /plugin marketplace add caramelotech/caramelo-skills
   ```

   Ou direto do terminal, com a CLI:

   ```bash
   claude plugin marketplace add caramelotech/caramelo-skills
   ```

   Outras formas de apontar para o mesmo repositório, com qualquer um dos dois comandos acima:

   ```
   # via SSH
   git@github.com:caramelotech/caramelo-skills.git

   # caminho local
   /caminho/para/caramelo-skills
   ```

2. Instale a categoria que você precisa:

   ```
   /plugin install development@caramelo-skills
   /plugin install writing@caramelo-skills
   /plugin install devops@caramelo-skills
   /plugin install design@caramelo-skills
   /plugin install study@caramelo-skills
   /plugin install career@caramelo-skills
   ```

   As skills de uma categoria ficam disponíveis com o prefixo dela, por exemplo `/development:code-review`.

3. Para validar antes de publicar alterações:

   ```bash
   claude plugin validate .
   claude plugin validate ./skills/<categoria>
   ```

### Como contexto manual

Copie o conteúdo de um `SKILL.md` e use como contexto em qualquer LLM:

```bash
cat skills/<categoria>/skills/<nome-da-skill>/SKILL.md
```

### Agents

Os agents combinam múltiplas skills para tarefas complexas. Cada um tem seu próprio `README.md` com instruções detalhadas:

- [`code-reviewer`](agents/code-reviewer/README.md) - Revisão completa: qualidade + segurança
- [`test-generator`](agents/test-generator/README.md) - Geração de suite de testes para um módulo
- [`doc-writer`](agents/doc-writer/README.md) - Geração de documentação técnica

## Preferências

Algumas categorias lembram as preferências de cada pessoa entre sessões, para não perguntar tudo de novo a cada uso. As preferências ficam em arquivos na pasta do usuário, nunca neste repositório:

| Categoria     | Arquivo                                  | O que guarda                                                                                         |
| ------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `development` | `~/.claude/development/preferences.json` | Modo de autonomia, comportamento de cada skill (commits, push, correções, testes) e ajustes por repositório |
| `career`      | `~/.claude/career/profile.json`          | Trajetória profissional, pasta de destino, idioma, formatos e objetivo de carreira                   |
| `study`       | `~/.claude/lecture-notes/courses.json`   | Cursos e pastas onde ficam as notas de cada um                                                       |

Para mudar uma preferência, use `--reconfigurar` na skill, `--preferencias` para ver as atuais (em `development`) ou peça em linguagem natural.

## Versionamento

O repositório segue [Versionamento Semântico](https://semver.org/lang/pt-BR/) em dois níveis:

- **Marketplace** (`.claude-plugin/marketplace.json`, campo `version`): versão geral do catálogo de categorias.
- **Categoria** (`skills/<categoria>/.claude-plugin/plugin.json`, campo `version`): versão própria de cada categoria, incrementada apenas quando ela muda.

Todas as mudanças notáveis são documentadas em [`CHANGELOG.md`](CHANGELOG.md), seguindo [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## Contribuindo

Quer adicionar uma skill, um agent ou uma categoria nova? Veja o guia em [CONTRIBUTING.md](.github/CONTRIBUTING.md).
