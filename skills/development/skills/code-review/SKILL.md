---
name: code-review
description: Revisa código em busca de bugs, vulnerabilidades de segurança, problemas de performance e manutenibilidade. Lembra as preferências da pessoa entre sessões (onde entregar a revisão, severidade mínima, se deve só sugerir, perguntar ou aplicar as correções, e se inclui a checagem OWASP), para trabalhar de forma autônoma quando ela quiser. Use quando for solicitado revisar, analisar ou dar feedback sobre código.
allowed-tools:
  - Read(~/.claude/plugins/**/caramelo-skills/**)
  - Read(~/.claude/development/preferences.json)
  - Edit(~/.claude/development/preferences.json)
  - Bash(git status --short)
  - Bash(git diff --no-ext-diff *)
  - Bash(git log --oneline *)
  - Bash(git remote get-url origin)
  - Bash(git rev-parse --show-toplevel)
  - Skill
  - AskUserQuestion
---

# Code Review

Revise o código fornecido com foco em corretude, segurança, legibilidade e manutenibilidade, seguindo boas práticas da linguagem utilizada.

## 0. Preferências

Leia e siga `../../shared/preferences.md` (caminho relativo à pasta desta skill). Esta skill usa `autonomy` e as preferências abaixo, em `skills.code-review` (ou em `repos.<repositório>.code-review`, que têm prioridade):

| Preferência   | Valores                             | Padrão     | O que controla                                                                                                                          |
| ------------- | ----------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `output`      | `chat`, `file`                      | `chat`     | Entregar a revisão no chat ou num arquivo `code-review-<YYYY-MM-DD>.md` (na pasta `outputPath`, se definida, ou na raiz do repositório) |
| `minSeverity` | `sugestao`, `importante`, `critico` | `sugestao` | Severidade mínima dos itens listados                                                                                                    |
| `fixes`       | `suggest`, `ask`, `apply`           | `suggest`  | Só sugerir correções, perguntar antes de aplicá-las, ou aplicar automaticamente as `crítico` e `importante`                              |
| `withOwasp`   | `true`, `false`                     | `false`    | Rodar também a skill `owasp-check` e juntar os achados na seção de segurança                                                            |

Perguntas da configuração inicial (junto com a de autonomia, se faltar):

- **Correções** (header `Correções`): `Só sugerir` (Recommended), `Perguntar antes de aplicar`, `Aplicar automaticamente`.
- **Saída** (header `Saída`): `No chat` (Recommended), `Em arquivo`.
- **Severidade** (header `Severidade`): `Tudo, inclusive sugestões` (Recommended), `Só importante e crítico`, `Só crítico`.

`withOwasp` começa em `false` e muda por reconfiguração ou pedido ("sempre inclua a checagem de segurança").

Flags (têm prioridade sobre as preferências, só nesta chamada): `--reconfigurar` refaz as perguntas de preferências; `--preferencias` mostra as preferências em uso e não executa a tarefa.

### Aplicar correções

- **`suggest`**: só liste as correções.
- **`ask`**: no modo `assistido`, ao final pergunte quais correções aplicar. No modo `autonomo` ou sem ninguém para responder, use o padrão seguro (só sugerir) e informe.
- **`apply`**: aplique as correções `crítico` e `importante` com a menor mudança possível, sem refatorar além do necessário. Sugestões de estilo nunca são aplicadas automaticamente. Depois, rode os testes e o lint do projeto, se existirem, e informe o resultado. Se uma correção depender de decisão de negócio ou de contexto ausente, não aplique: deixe como sugestão e explique.

## Princípios de execução

Para reduzir erros comuns de assistentes de IA ao revisar código, siga estes princípios. Para revisões triviais, use bom senso - o trade-off aqui é cautela em vez de velocidade.

**Pense antes de apontar um problema**
Não presuma a intenção do autor do código. Se uma sugestão depender de contexto ausente (requisito de negócio, decisão de arquitetura, biblioteca específica), diga isso explicitamente em vez de aplicar uma interpretação silenciosa. Se houver mais de uma leitura razoável do código, apresente as alternativas.

**Simplicidade em primeiro lugar**
Ao sugerir uma correção, proponha a menor mudança que resolve o problema. Não recomende abstrações, flexibilidade ou tratamento de erro para cenários que o código não precisa cobrir - isso é um problema novo, não parte da revisão.

**Separe bug de preferência de estilo**
Não trate "eu faria diferente" como "isto está errado". Classifique com cuidado entre `crítico`/`importante` (corretude, segurança, performance real) e `sugestão` (legibilidade, nomenclatura). Não sugira refatorar código que já funciona só porque você escolheria outra abordagem.

**Torne o problema verificável**
Para cada item crítico ou importante, diga como reproduzi-lo (entrada que dispara o bug, cenário de ataque) e como confirmar que a correção resolve.

## Como revisar

Organize a revisão nas seguintes categorias:

**Bugs e corretude**
Liste problemas que causam ou podem causar comportamento incorreto.

**Segurança**
Aponte vulnerabilidades (injeção, exposição de dados, permissões, etc.).

**Performance**
Identifique gargalos ou operações desnecessariamente custosas.

**Legibilidade e manutenção**
Sugira melhorias de nomenclatura, estrutura e clareza.

**Pontos positivos**
Destaque o que está bem implementado.

Para cada problema encontrado, informe:

- Severidade: `crítico` | `importante` | `sugestão`
- Linha ou trecho afetado
- Sugestão de correção

## Variáveis

| Variável        | Descrição             | Exemplo                          |
| --------------- | --------------------- | -------------------------------- |
| `{{linguagem}}` | Linguagem do código   | `TypeScript`                     |
| `{{contexto}}`  | O que o código faz    | `Middleware de autenticação JWT` |
| `{{codigo}}`    | Código a ser revisado | _(trecho ou diff)_               |

## Exemplo

**Input:**

```python
# linguagem: Python
# contexto: Função que valida e salva usuário no banco

def save_user(name, email, db):
    query = f"INSERT INTO users VALUES ('{name}', '{email}')"
    db.execute(query)
```

**Output esperado:**

```
**Bugs e corretude**
- A ausência de tratamento de erro em db.execute pode causar falhas silenciosas.

**Segurança**
- [CRÍTICO] Linha 2: SQL Injection via interpolação direta de variáveis na query.
  Correção: db.execute("INSERT INTO users VALUES (?, ?)", (name, email))

**Performance**
- Sem problemas evidentes para o escopo atual.

**Legibilidade e manutenção**
- [SUGESTÃO] Adicione validação dos inputs antes de persistir.

**Pontos positivos**
- Assinatura simples e responsabilidade única bem definida.
```

## Notas

- Para diffs grandes, revise por arquivo ou por função
- Informe o contexto do PR para revisões mais precisas
- Combine com a skill `owasp-check` para revisões focadas em segurança, ou ative `withOwasp` para rodá-la sempre
- Ao final, informe o que foi aplicado (se houve), onde a revisão foi salva (se em arquivo) e, na primeira execução, onde as preferências foram salvas e como mudá-las
