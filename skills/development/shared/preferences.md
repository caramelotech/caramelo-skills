# Preferências de desenvolvimento

Procedimento compartilhado pelas skills da categoria `development` (`commit-message`, `code-review`, `owasp-check`, `unit-test-generator`, `technical-cofounder`, `bruno-collection`). Cada skill aponta para este arquivo e segue as instruções abaixo antes de começar a tarefa.

O objetivo é que a pessoa decida uma vez como quer trabalhar e a skill respeite isso nas próximas chamadas: se ela quiser, o agente trabalha de forma independente, sem parar para esperar respostas.

## Arquivo de preferências

As preferências são a memória das skills de desenvolvimento entre sessões. É um arquivo global, único para todas as skills da categoria, para funcionar de qualquer diretório:

```
~/.claude/development/preferences.json
```

```json
{
  "autonomy": "autonomo",
  "skills": {
    "commit-message": {
      "protectedBranches": ["main", "master", "develop", "developer"],
      "protectedBranchPolicy": "ask",
      "confirmPlan": "inherit",
      "push": "never",
      "signoff": false,
      "language": "en"
    },
    "code-review": {
      "output": "chat",
      "minSeverity": "sugestao",
      "fixes": "suggest",
      "withOwasp": false
    },
    "owasp-check": {
      "output": "chat",
      "fixes": "suggest"
    },
    "unit-test-generator": {
      "output": "write",
      "runTests": true,
      "naming": "project"
    },
    "bruno-collection": {
      "secretStrategy": "dotenv",
      "environments": ["local"]
    }
  },
  "repos": {
    "github.com/caramelotech/caramelo-skills": {
      "commit-message": { "protectedBranchPolicy": "allow" },
      "unit-test-generator": { "framework": "vitest", "testDir": "src/**/__tests__" },
      "bruno-collection": { "collectionPath": ".bruno", "format": "yml" }
    }
  },
  "updated": "2026-10-10"
}
```

### Modo de autonomia (`autonomy`)

Vale para todas as skills da categoria.

| Valor       | Comportamento                                                                                                                                                                                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `assistido` | A skill apresenta o plano e espera confirmação antes de qualquer efeito (commit, escrita de arquivos, aplicação de correções)                                                                                                                                           |
| `autonomo`  | A skill executa com as preferências salvas, sem esperar resposta, e mostra no final o que fez e por quê. Quando uma decisão não estiver coberta por uma preferência, escolhe a opção mais segura (veja "Padrões seguros") e registra a escolha no relatório final |

Mesmo no modo `autonomo`, a skill **sempre para e pergunta** antes de:

- reescrever histórico já publicado (`git push --force`, `rebase` de commits enviados, `reset` de commits enviados);
- apagar arquivos, branches ou dados que não foram criados por ela na mesma execução;
- qualquer ação que uma regra inegociável da skill proíba (por exemplo, commitar segredos).

Nesses casos, se a pessoa não estiver disponível, a skill não faz a ação e registra o motivo no relatório final, em vez de ficar bloqueada.

### Padrões seguros

Quando uma decisão não estiver coberta por preferência e não houver como perguntar (modo `autonomo` ou execução não interativa), use:

- commitar em branch protegida: criar uma branch nova (`<tipo>/<descricao-curta>`) em vez de commitar direto;
- push: não fazer;
- correções de código: sugerir, não aplicar;
- arquivos de saída: não sobrescrever arquivos existentes que a skill não criou.

### Preferências por repositório (`repos`)

Algumas preferências mudam de um repositório para outro (por exemplo, permitir commit direto na `main` só em repositórios pessoais). A chave do repositório é a URL do remoto `origin` sem protocolo, usuário e `.git` (ex: `github.com/caramelotech/caramelo-skills`), ou o caminho absoluto da raiz do repositório quando não houver remoto.

Ordem de precedência, da mais forte para a mais fraca: flag da chamada, preferência do repositório, preferência da skill, `autonomy` global, padrão seguro.

## Ao iniciar qualquer skill da categoria

1. Leia `~/.claude/development/preferences.json`. Se estiver dentro de um repositório git, descubra a chave do repositório e leia também as preferências dele em `repos`.
2. Se o arquivo existir e tiver `autonomy` e as preferências que a skill usa, **não faça nenhuma pergunta de configuração**: siga direto para a tarefa.
3. Se faltar `autonomy` ou alguma preferência da skill, ou se vier `--reconfigurar`, faça a configuração inicial abaixo, **perguntando só o que falta**. Uma pessoa que já usou outra skill da categoria não responde de novo a pergunta de autonomia.
4. Se a execução não for interativa (sem `AskUserQuestion` e sem ninguém para responder), não pergunte: use os padrões seguros, execute e informe no relatório final quais preferências faltaram e como configurá-las.

## Configuração inicial

Use a ferramenta `AskUserQuestion`, com até 4 perguntas na mesma chamada:

- **Autonomia** (header `Autonomia`), se faltar `autonomy`:
  - `Assistido` (Recommended): "Mostra o plano e espera sua confirmação antes de commitar, escrever arquivos ou aplicar correções".
  - `Autônomo`: "Executa com as suas preferências, sem esperar resposta, e mostra no final o que fez".
- As perguntas específicas da skill, conforme a seção de preferências de cada `SKILL.md`, até completar 4. Preferências que não couberem na chamada recebem o valor padrão da skill e podem ser mudadas depois.

Grave o arquivo (com `updated` igual à data de hoje) e siga com a tarefa. Se a `AskUserQuestion` não estiver disponível, faça as mesmas perguntas em texto, com as opções numeradas.

## Reconfigurar

A pessoa pode mudar preferências a qualquer momento, de três formas:

- **`--reconfigurar`** em qualquer skill da categoria: refaz as perguntas daquela skill (e a de autonomia), mostrando os valores atuais como opção recomendada.
- **`--preferencias`** em qualquer skill da categoria: mostra as preferências atuais (globais, da skill e do repositório atual) numa tabela curta e não executa a tarefa.
- **Pedido em linguagem natural**, como "pode commitar direto na main neste repositório", "não precisa mais confirmar os commits" ou "volte a me perguntar antes de aplicar correções": atualize só o campo correspondente. Se o pedido mencionar "neste repositório", grave em `repos`; caso contrário, grave na preferência da skill. Confirme em uma linha o que mudou.

## Regras do arquivo

- Guarde só preferências. Nunca grave código, diffs, segredos, tokens ou conteúdo dos repositórios.
- Se o agente tiver um sistema de memória persistente próprio (por exemplo, a memória do Claude Code), registre lá também um ponteiro curto: "Preferências das skills de desenvolvimento ficam em `~/.claude/development/preferences.json`". O arquivo continua sendo a fonte da verdade.
- Na primeira execução, o relatório final da skill diz onde as preferências foram salvas e como mudá-las.
