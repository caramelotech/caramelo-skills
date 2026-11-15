# Agent: Doc Writer

**Tipo:** assistido  
**Skills utilizadas:** `skills/development/skills/commit-plan/SKILL.md`

## Objetivo

Gera documentação técnica a partir do código-fonte: README, docstrings, changelogs e guias de uso.

## Fluxo de execução

```
1. Recebe o código-fonte e o tipo de documentação desejada
2. Analisa a estrutura do código (funções, classes, parâmetros, retornos)
3. Gera a documentação no formato solicitado
4. Adapta o nível de detalhe para o público-alvo informado
```

## Como usar

Informe o código, o tipo de documento desejado e o público-alvo. O agente retornará a documentação formatada e pronta para uso.

## Inputs

| Parâmetro       | Obrigatório | Descrição                                        |
| --------------- | ----------- | ------------------------------------------------- |
| `codigo`        | Sim         | Código-fonte a documentar                        |
| `tipo`          | Sim         | `readme`, `docstring`, `changelog`, `guia`       |
| `publico`       | Sim         | `desenvolvedor`, `usuário final`, `contribuidor` |
| `linguagem_doc` | Não         | Idioma da documentação (padrão: português)       |

## Output

Documentação formatada em Markdown pronta para ser inserida no repositório ou no código.
