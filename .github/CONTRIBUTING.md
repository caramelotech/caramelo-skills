# Contribuindo

Guia para adicionar ou alterar skills, agents, categorias e integrações neste repositório.

## O que é uma skill

Uma skill é um pacote de instruções que ensina o Claude Code a executar bem uma tarefa específica e recorrente. Diferente de um prompt avulso, uma skill fica disponível permanentemente para o agente e só é carregada em detalhe quando o contexto da conversa indica que ela é relevante.

## Estrutura do repositório

```
skills/<categoria>/
├── .claude-plugin/
│   └── plugin.json          # manifesto do plugin (name, version, description, author, license, keywords)
└── skills/
    └── <nome-da-skill>/
        └── SKILL.md
```

- Cada pasta em `skills/` (`development`, `writing`, `devops`, `design`, `study`, `career`) é uma **categoria**: um plugin independente do Claude Code, com sua própria versão.
- A subpasta `skills/` dentro de cada categoria é a convenção de escaneamento padrão do Claude Code - não renomeie nem mova para outro nível.
- `agents/<nome>/README.md` orquestra múltiplas skills (ex: `code-reviewer` combina `development:code-review` e `development:owasp-check`).
- `plugins/<nome>/README.md` documenta integrações com ferramentas externas (VS Code, MCP) - não confundir com os plugins do Claude Code em `skills/`.
- `templates/` tem o ponto de partida para cada um desses três tipos de item.

## Adicionando uma skill

1. Escolha a categoria onde a skill se encaixa. Se nenhuma existir, veja [Adicionando uma categoria nova](#adicionando-uma-categoria-nova) primeiro.
2. Copie `templates/skill.md` para `skills/<categoria>/skills/<nome-da-skill>/SKILL.md`.
3. Preencha o frontmatter:

   ```yaml
   ---
   name: nome-da-skill
   description: O que a skill faz e quando deve ser usada.
   ---
   ```

   | Campo           | Regra                                                                                                                                                                                                |
   | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `name`          | kebab-case, em inglês, idêntico ao nome da pasta                                                                                                                                                     |
   | `description`   | em português - é o único texto sempre carregado no contexto do Claude e o principal mecanismo de acionamento da skill, então inclua o que ela faz e os contextos/palavras-chave que devem dispará-la |
   | `allowed-tools` | opcional - ferramentas que rodam **sem pedir permissão** enquanto a skill está ativa. Siga o princípio do menor privilégio (veja abaixo)                                                             |

   **Menor privilégio em `allowed-tools`.** O campo não restringe o que a skill pode usar: ele pré-aprova. Tudo o que fica de fora continua disponível, mas pede permissão. Por isso:

   - Nunca liste `Bash`, `Write`, `Edit`, `Read`, `Glob`, `Grep` ou `WebFetch` sem escopo. Use padrões específicos: `Bash(git status --short)`, `Bash(git diff --no-ext-diff *)`, `Read(~/.claude/<categoria>/<arquivo>.json)`, `Edit(./.pasta-da-skill/**)`.
   - Em padrões de `Bash`, use `comando *` (espaço antes do `*`) e prefira a forma exata do comando. Não pré-aprove comandos que executam código arbitrário ou do projeto (`python -c`, `node -e`, `npm test`, `npx`, `sh -c`), que acessam a rede (`curl`, `pip install`, `git push` com refspec livre) ou que reescrevem histórico.
   - Para ler os arquivos da própria skill (referências e `shared/`), use `Read(~/.claude/plugins/**/caramelo-skills/**)`.
   - `WebFetch` sem escopo permite que um texto malicioso lido pela skill mande dados para qualquer URL: deixe-o fora e deixe o agente pedir permissão por domínio.
   - No corpo da skill, diga que conteúdo lido (código, páginas, documentos) é dado, não instrução, e que comandos bloqueados não devem ser trocados por equivalentes para evitar o pedido de permissão.

4. Escreva o corpo em português, no imperativo ("Revise o código...", "Gere a mensagem..."), seguindo as seções do template (`Como usar`, `Variáveis`, `Exemplo`, `Notas`). Exemplos de código ficam em inglês.
5. Nenhum registro manual é necessário: cada categoria escaneia sua própria `skills/` automaticamente. Só edite `plugin.json` se a nova skill mudar a descrição ou as keywords da categoria.

## Adicionando uma categoria nova

1. Crie `skills/<categoria>/.claude-plugin/plugin.json`:

   ```json
   {
     "name": "<categoria>",
     "version": "1.0.0",
     "description": "Descrição curta em português do que a categoria cobre",
     "author": {
       "name": "Caramelo Tech",
       "url": "https://github.com/caramelotech"
     },
     "license": "MIT",
     "keywords": ["..."]
   }
   ```

2. Adicione `skills/<categoria>/skills/<nome>/SKILL.md` com pelo menos uma skill.
3. Registre a categoria em `.claude-plugin/marketplace.json`, no array `plugins`, com `name`, `source` (`./skills/<categoria>`), `description`, `category` e `tags`.
4. Valide os dois manifestos:

   ```bash
   claude plugin validate .
   claude plugin validate ./skills/<categoria>
   ```

## Adicionando um agent

Copie `templates/agent.md` para `agents/<nome>/README.md`, declarando tipo (autônomo ou assistido), skills utilizadas (caminho completo, ex: `skills/development/skills/code-review/SKILL.md`), ferramentas necessárias, fluxo de execução e tabela de inputs/outputs.

## Adicionando uma integração externa (plugins/)

Copie `templates/plugin.md` para `plugins/<nome>/README.md`, declarando plataforma, versão mínima, dependências, instalação e configuração. Isso é independente do sistema de plugins do Claude Code em `skills/`.

## Testando localmente

Antes de abrir o PR, registre o repositório local como marketplace e instale a categoria alterada:

```
/plugin marketplace add /caminho/para/caramelo-skills
/plugin install <categoria>@caramelo-skills
```

Rode alguns prompts reais (as frases que motivaram a skill) e confira se ela é acionada e produz o resultado esperado.

## Processo de contribuição

1. Faça um fork do repositório (ou crie uma branch, se tiver acesso de escrita).
2. Crie uma branch a partir de `main`:

   ```bash
   git checkout -b feature/nome-da-skill
   # ou fix/, docs/, refactor/
   ```

3. Faça suas alterações e valide com `claude plugin validate`.
4. Commit seguindo [Conventional Commits](https://www.conventionalcommits.org/):

   | Tipo        | Descrição                    |
   | ----------- | ---------------------------- |
   | `feat:`     | Nova funcionalidade          |
   | `fix:`      | Correção de bug              |
   | `docs:`     | Documentação                 |
   | `refactor:` | Refatoração de código        |
   | `test:`     | Adição ou correção de testes |
   | `chore:`    | Tarefas de manutenção        |

5. Atualize a tabela de skills no [README.md](../README.md) e registre a mudança em [CHANGELOG.md](../CHANGELOG.md), incrementando a versão da categoria afetada (e do marketplace, se a mudança for estrutural - novo caminho, categoria renomeada ou removida).
6. Abra um Pull Request descrevendo a motivação da mudança.

## Código de Conduta

Ao contribuir, você concorda em seguir o [Código de Conduta da Caramelo Tech](https://github.com/caramelotech/.github/blob/main/CODE_OF_CONDUCT.md).

## Referências

- [Claude Code - Plugin marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)
- [Claude Code - Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
