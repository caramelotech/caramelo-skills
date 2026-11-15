---
name: owasp-check
description: Analisa código em busca de vulnerabilidades de segurança do OWASP Top 10, com classificação de severidade e exemplos de correção. Lembra as preferências da pessoa entre sessões (onde entregar o relatório, severidade mínima e se deve só sugerir, perguntar ou aplicar as correções), para trabalhar de forma autônoma quando ela quiser. Use quando for solicitada uma revisão de segurança, identificação de vulnerabilidades ou auditoria de segurança do código.
allowed-tools:
  - Read(~/.claude/plugins/**/caramelo-skills/**)
  - Read(~/.claude/development/preferences.json)
  - Edit(~/.claude/development/preferences.json)
  - Bash(git status --short)
  - Bash(git diff --no-ext-diff *)
  - Bash(git log --oneline *)
  - Bash(git remote get-url origin)
  - Bash(git rev-parse --show-toplevel)
  - AskUserQuestion
---

# OWASP Security Check

## Preferências

Leia e siga `../../shared/preferences.md` (caminho relativo à pasta desta skill). Esta skill usa `autonomy` e as preferências abaixo, em `skills.owasp-check` (ou em `repos.<repositório>.owasp-check`, que têm prioridade):

| Preferência   | Valores                             | Padrão    | O que controla                                                                                                                          |
| ------------- | ----------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `output`      | `chat`, `file`                      | `chat`    | Entregar no chat ou num arquivo `owasp-check-<YYYY-MM-DD>.md` (na pasta `outputPath`, se definida, ou na raiz do repositório)            |
| `minSeverity` | `baixa`, `media`, `alta`, `critica` | `baixa`   | Severidade mínima das vulnerabilidades listadas                                                                                         |
| `fixes`       | `suggest`, `ask`, `apply`           | `suggest` | Só sugerir correções, perguntar antes de aplicá-las, ou aplicar automaticamente as `Crítica` e `Alta`                                    |

Perguntas da configuração inicial (junto com a de autonomia, se faltar):

- **Correções** (header `Correções`): `Só sugerir` (Recommended), `Perguntar antes de aplicar`, `Aplicar automaticamente`.
- **Saída** (header `Saída`): `No chat` (Recommended), `Em arquivo`.
- **Severidade** (header `Severidade`): `Todas` (Recommended), `Média ou maior`, `Alta ou maior`.

Flags (têm prioridade sobre as preferências, só nesta chamada): `--reconfigurar` refaz as perguntas de preferências; `--preferencias` mostra as preferências em uso e não executa a tarefa.

Aplicação de correções:

- **`suggest`**: só liste as correções.
- **`ask`**: no modo `assistido`, ao final pergunte quais aplicar. No modo `autonomo` ou sem ninguém para responder, só sugira e informe.
- **`apply`**: aplique as correções `Crítica` e `Alta` com a menor mudança possível e rode os testes do projeto, se existirem. Correções que mudam comportamento visível (por exemplo, exigir autenticação numa rota pública) ou dependem de decisão de negócio nunca são aplicadas sem confirmação: deixe como sugestão e explique.

Ao final, informe o que foi aplicado (se houve), onde o relatório foi salvo (se em arquivo) e, na primeira execução, onde as preferências foram salvas e como mudá-las.

## Análise

Analise o código fornecido em busca de vulnerabilidades do OWASP Top 10 (2021). Para cada vulnerabilidade encontrada, informe:

- **Categoria OWASP:** (ex: A03 - Injection)
- **Severidade:** `Crítica` | `Alta` | `Média` | `Baixa`
- **Evidência:** trecho exato do código vulnerável
- **Risco:** o que um atacante pode fazer com essa vulnerabilidade
- **Correção:** como corrigir, com exemplo de código seguro

Ao final, atribua uma **nota geral de segurança de 0 a 10** e escreva um **resumo executivo em 2-3 frases**.

Se nenhuma vulnerabilidade for encontrada, confirme explicitamente e destaque as boas práticas presentes no código.

## Variáveis

| Variável             | Descrição              | Exemplo                            |
| -------------------- | ---------------------- | ---------------------------------- |
| `{{linguagem}}`      | Linguagem do código    | `Node.js`                          |
| `{{tipo_aplicacao}}` | Tipo da aplicação      | `API REST`, `aplicação web`, `CLI` |
| `{{codigo}}`         | Código a ser analisado | _(trecho ou arquivo)_              |

## Exemplo

**Input:**

```javascript
// linguagem: Node.js
// tipo_aplicacao: API REST

app.get('/user', (req, res) => {
  const id = req.query.id;
  db.query(`SELECT * FROM users WHERE id = ${id}`, (err, result) => {
    res.json(result);
  });
});
```

**Output esperado:**

```
**A03 - Injection**
- Severidade: Crítica
- Evidência: `SELECT * FROM users WHERE id = ${id}`
- Risco: Atacante pode extrair, modificar ou deletar dados do banco via SQL Injection
- Correção: usar prepared statements
  db.query('SELECT * FROM users WHERE id = ?', [id], callback)

**A01 - Broken Access Control**
- Severidade: Alta
- Evidência: ausência de autenticação/autorização na rota
- Risco: qualquer usuário pode consultar dados de qualquer outro usuário
- Correção: adicionar middleware de autenticação antes do handler

Nota geral: 2/10
Resumo: O endpoint expõe dados sensíveis sem autenticação e é criticamente vulnerável a
SQL Injection. Corrija esses dois pontos antes de qualquer deploy em produção.
```

## Notas

- Analise arquivos menores que 200 linhas por vez para resultados mais precisos
- Combine com ferramentas estáticas (Semgrep, Bandit, ESLint Security) para cobertura completa
- Priorize vulnerabilidades Críticas e Altas antes de qualquer deploy
- Combine com a skill `code-review` para uma análise completa de qualidade e segurança
