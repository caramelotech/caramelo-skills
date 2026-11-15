---
name: unit-test-generator
description: Gera testes unitários para uma função ou classe, cobrindo caminho feliz, casos de borda e cenários de erro. Lembra as preferências da pessoa entre sessões (escrever os arquivos de teste ou só mostrar no chat, rodar os testes, padrão de nomes) e o framework e a pasta de testes de cada repositório, para trabalhar de forma autônoma quando ela quiser. Use quando for solicitado escrever, criar ou gerar testes.
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

# Unit Test Generator

Gere uma suite completa de testes unitários para o código fornecido, cobrindo caminho feliz, casos de borda e cenários de erro.

## Preferências

Leia e siga `../../shared/preferences.md` (caminho relativo à pasta desta skill). Esta skill usa `autonomy` e as preferências abaixo, em `skills.unit-test-generator` (ou em `repos.<repositório>.unit-test-generator`, que têm prioridade):

| Preferência | Valores                                 | Padrão    | O que controla                                                                                                                                  |
| ----------- | --------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `output`    | `write`, `chat`                         | `write`   | Escrever o arquivo de teste no repositório, seguindo a convenção do projeto, ou só mostrar o código no chat                                      |
| `runTests`  | `true`, `false`                         | `true`    | Rodar os testes gerados depois de escrevê-los                                                                                                   |
| `naming`    | `project`, `deve_quando`, `should_when` | `project` | Seguir o padrão de nomes dos testes que já existem no projeto, ou usar `deve_[resultado]_quando_[condição]` ou `should_[result]_when_[condition]` |
| `framework` | nome do framework (por repositório)     | detectado | Framework de testes do repositório                                                                                                              |
| `testDir`   | padrão de pasta (por repositório)       | detectado | Onde ficam os testes do repositório                                                                                                             |

Perguntas da configuração inicial (junto com a de autonomia, se faltar):

- **Saída** (header `Saída`): `Escrever os arquivos de teste` (Recommended), `Só mostrar no chat`.
- **Rodar testes** (header `Rodar`): `Rodar depois de escrever` (Recommended), `Não rodar`.
- **Nomes** (header `Nomes`): `Seguir o padrão do projeto` (Recommended), `deve_..._quando_...`, `should_..._when_...`.

`framework` e `testDir` não são perguntados: detecte-os no repositório (dependências, arquivos de configuração e testes existentes) e grave em `repos.<repositório>.unit-test-generator` para não detectar de novo. Se não houver testes nem framework no repositório, recomende o framework mais comum da linguagem; no modo `assistido`, confirme antes de instalar qualquer dependência, e no modo `autonomo` não instale: escreva os testes, informe o comando para instalar e não rode.

Flags (têm prioridade sobre as preferências, só nesta chamada): `--reconfigurar` refaz as perguntas de preferências; `--preferencias` mostra as preferências em uso e não executa a tarefa.

### Escrever e rodar

- Com `output` igual a `write`: no modo `assistido`, mostre onde o arquivo será criado e confirme antes de escrever; no modo `autonomo`, escreva direto. Nunca sobrescreva um arquivo de teste existente: acrescente os testes novos a ele ou crie outro arquivo, e informe.
- Com `runTests` ativo: rode só os testes gerados. Se algum falhar por erro no próprio teste, corrija o teste. Se falhar porque o código testado tem um bug, **não altere o código testado**: mantenha o teste, marque-o como falhando e explique o bug encontrado no relatório final.
- Ao final, informe os arquivos criados ou alterados, o resultado dos testes e, na primeira execução, onde as preferências foram salvas e como mudá-las.

## Como gerar os testes

- Cubra o caminho feliz (happy path)
- Cubra casos de borda (valores nulos, vazios, extremos)
- Cubra cenários de erro e exceções esperadas
- Use nomes descritivos conforme a preferência `naming` (por padrão, o padrão dos testes que já existem no projeto; sem testes existentes, `deve_[resultado]_quando_[condição]`)
- Adicione um comentário de uma linha explicando cada grupo de testes
- Não use mocks a menos que sejam estritamente necessários para isolar dependências externas

Com `output` igual a `chat`, retorne apenas o código dos testes, sem explicações adicionais. Com `write`, escreva o arquivo e entregue o relatório curto descrito em "Escrever e rodar".

## Variáveis

| Variável        | Descrição                 | Exemplo              |
| --------------- | ------------------------- | -------------------- |
| `{{linguagem}}` | Linguagem do código       | `Python`             |
| `{{framework}}` | Framework de testes       | `pytest`             |
| `{{codigo}}`    | Função ou classe a testar | _(trecho de código)_ |

## Exemplo

**Input:**

```python
# linguagem: Python
# framework: pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Divisor cannot be zero")
    return a / b
```

**Output esperado:**

```python
import pytest
from math import isclose
from module import divide

# Happy path
def test_deve_retornar_quociente_quando_divisao_valida():
    assert isclose(divide(10, 2), 5.0)

def test_deve_retornar_float_quando_resultado_nao_inteiro():
    assert isclose(divide(1, 3), 0.3333, rel_tol=1e-4)

# Edge cases
def test_deve_retornar_zero_quando_numerador_zero():
    assert divide(0, 5) == 0

def test_deve_funcionar_com_numeros_negativos():
    assert isclose(divide(-10, 2), -5.0)

def test_deve_funcionar_com_dois_negativos():
    assert isclose(divide(-10, -2), 5.0)

# Error scenarios
def test_deve_lancar_valueerror_quando_divisor_zero():
    with pytest.raises(ValueError, match="Divisor cannot be zero"):
        divide(10, 0)
```

## Notas

- Para classes, solicite testes por método para manter o escopo gerenciável
- Especifique se o projeto usa fixtures ou factories para dados de teste
- Mensagens de erro e strings internas do código devem estar em inglês para manter consistência com o código-fonte
