---
name: linkedin-review
description: Avalia um perfil do LinkedIn contra um objetivo de carreira e gera um relatório .md com ajustes sugeridos por seção (título, Sobre, Experiência, competências e palavras-chave, Destaques, simulação de recrutador e DMs de prospecção), cada um com o racional da decisão. No primeiro uso coleta o link do perfil, o setor, o cargo-alvo e as empresas-alvo, e guarda no perfil de carreira compartilhado; nas próximas rodadas reaproveita tudo e compara com a avaliação anterior. Usa a trajetória profissional salva para completar métricas sem inventar. Use quando a pessoa pedir para revisar, auditar, otimizar ou reescrever o perfil do LinkedIn, ou para atrair recrutadores.
allowed-tools:
  - Read(~/.claude/plugins/**/caramelo-skills/**)
  - Read(~/.claude/career/profile.json)
  - Edit(~/.claude/career/profile.json)
  - Skill
  - AskUserQuestion
---

# Avaliação de perfil do LinkedIn

Audita um perfil do LinkedIn contra um objetivo de carreira e entrega um relatório `.md` com todos os ajustes sugeridos, mapeados por seção e com o racional de cada decisão. O relatório existe para a pessoa entender **por que** cada mudança foi proposta, não só copiar o texto novo.

A skill é genérica: no primeiro uso ela coleta o objetivo de carreira e onde está o perfil, e guarda essas informações no perfil de carreira compartilhado com as outras skills da categoria. Nas rodadas seguintes, basta chamar a skill.

## Parâmetros

Todos são opcionais na chamada: o que não vier é lido do perfil salvo ou perguntado no primeiro uso.

| Parâmetro         | Flag         | O que é                                                                                                                 |
| ----------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `[perfil]`        | `--perfil`   | URL do perfil (`https://www.linkedin.com/in/...`), caminho de um PDF ou arquivo com o conteúdo do perfil, ou texto colado |
| `[setor]`         | `--setor`    | Setor de referência (ex: fintech, saúde, educação). Calibra o título e o tom                                            |
| `[cargo-alvo]`    | `--cargo`    | Cargo que a pessoa quer conquistar. Guia palavras-chave, Destaques e o critério de avaliação                           |
| `[empresas-alvo]` | `--empresas` | Uma ou mais empresas dos sonhos, separadas por vírgula. Usadas na simulação de recrutador e nas DMs                     |
| `[output]`        | `--output`   | Pasta do relatório. Sobrescreve o perfil só nesta chamada                                                               |
| `--reconfigurar`  | -            | Refaz a configuração inicial do perfil e do objetivo de carreira                                                        |

## 1. Perfil e objetivo de carreira

Leia e siga `../../shared/profile.md` (caminho relativo à pasta desta skill). Esta skill usa os campos `name`, `careerSource`, `extraSources`, `outputFolder` e `language` do perfil compartilhado, e os campos próprios abaixo:

```json
{
  "linkedin": {
    "url": "https://www.linkedin.com/in/nome-sobrenome",
    "contentSource": "C:/Users/ana/Documents/Carreira/LinkedIn - Perfil.pdf",
    "contentDate": "2026-10-10"
  },
  "careerGoal": {
    "sector": "fintech",
    "role": "Engenharia de Software Sênior (backend)",
    "companies": ["Nubank", "Stone"]
  }
}
```

A trajetória profissional é opcional para esta skill (o insumo principal é o próprio perfil do LinkedIn), mas melhora muito o relatório: com ela, as sugestões usam números e resultados reais em vez de placeholders. Se `careerSource` não existir, não bloqueie a avaliação: siga sem ela e, na resposta final, sugira criá-la com o fluxo "Obter a trajetória profissional" do perfil compartilhado.

### Primeiro uso

Quando faltar `linkedin.url` ou `careerGoal`, peça em **uma única mensagem de chat**, neste formato, incluindo só as linhas que faltam, e aguarde:

```
Link do seu perfil no LinkedIn:
Setor de referência (ex: fintech, saúde, educação):
Cargo que você quer conquistar:
Empresas dos sonhos (até 3, separadas por vírgula):
```

Explique em uma frase por que o objetivo importa: sem setor, cargo e empresas o relatório vira genérico, e o valor está na aderência ao objetivo. Grave as respostas no perfil.

### Rodadas seguintes

- Não pergunte de novo o que está salvo. Abra a resposta com uma linha mostrando o objetivo em uso ("Avaliando para Engenharia de Software Sênior em fintech, mirando Nubank e Stone") e siga.
- Se vierem `--setor`, `--cargo` ou `--empresas` diferentes do salvo, use-os nesta rodada e, ao final, pergunte se a pessoa quer salvá-los como o novo objetivo padrão.

## 2. Obter o conteúdo do perfil

1. Se veio `--perfil` com arquivo ou texto, use-o.
2. Se há `linkedin.contentSource` salvo, mostre a data da cópia (`contentDate`) e pergunte se a pessoa quer usá-la ou enviar uma versão nova. Se ela já aplicou sugestões de uma rodada anterior, a cópia antiga não reflete o perfil atual: recomende enviar uma nova.
3. Caso contrário, tente ler a URL com `obsidian:defuddle` ou `WebFetch`.
4. Se o conteúdo vier vazio, for uma tela de login ou trouxer só o cabeçalho, **não invente o resto do perfil**. Explique que o LinkedIn bloqueia leitura sem login e peça uma destas opções:
   - exportar o perfil em PDF (no próprio perfil, botão "Mais" e depois "Salvar como PDF") e informar o caminho; ou
   - colar o texto das seções (título, Sobre, Experiência, Formação, Competências, Destaques).
5. Texto colado é salvo como `LinkedIn - Perfil.md` em `outputFolder`. Grave em `linkedin.contentSource` o caminho do PDF ou desse arquivo, e em `contentDate` a data de hoje.
6. Registre no relatório qual foi a fonte do conteúdo e quais seções não puderam ser avaliadas por falta de dado.

Nunca peça senha nem cookies de sessão, e nunca tente autenticar no LinkedIn.

## 3. Ler a trajetória

Se houver `careerSource`, siga "Ler a trajetória" do perfil compartilhado. Use a trajetória para:

- completar métricas, resultados e tecnologias que existem nela mas faltam no LinkedIn, marcados como `(da trajetória)`;
- apontar inconsistências entre as duas fontes (datas, cargos, empresas) como sinal de alerta.

## 4. Analisar

Avalie cada seção conforme [references/sections.md](references/sections.md), que detalha o que gerar, o formato do racional e as restrições de cada uma das 7 seções:

1. Título (headline)
2. Sobre
3. Experiência
4. Competências e palavras-chave
5. Teste do recrutador
6. Destaques
7. DMs de prospecção

## 5. Regras de integridade

Valem para todas as seções, porque um perfil com dado falso custa mais caro que um perfil modesto (processos seletivos e checagem de referências desmentem):

- **Não invente métricas, cargos, empresas, resultados nem certificações.** A fórmula XYZ pede números: use os da trajetória quando existirem; quando não, escreva o placeholder `[X%]`, `[N clientes]` etc. e registre em "Perguntas para você" o que a pessoa precisa levantar.
- Só reescreva com base no que o perfil, a trajetória ou a pessoa informaram. Ao inferir algo, marque como `(inferido - confirme)`.
- Escreva no idioma do perfil compartilhado (`language`), sem clichês vazios ("apaixonado por tecnologia", "profissional proativo"). Se o perfil do LinkedIn estiver em outro idioma, avise e pergunte se as sugestões devem seguir o idioma do perfil do LinkedIn.
- Seja neutro quanto a gênero quando possível ("atuo como", "minha experiência"), a menos que o perfil use gênero marcado de forma consistente.
- Na simulação de recrutador seja franco, mas baseie o veredito no conteúdo do perfil, não em suposições sobre a cultura da empresa. Se pesquisar a empresa, cite a fonte.

## 6. Montar o relatório

Use o modelo em [assets/report-template.md](assets/report-template.md). O relatório tem, nesta ordem: resumo executivo (diagnóstico geral e as 3 mudanças de maior impacto), evolução desde a última avaliação (se houver), uma seção por item da lista acima, perguntas pendentes para a pessoa e plano de aplicação priorizado.

Cada seção segue o mesmo esqueleto: **Situação atual**, **Problema**, **Sugestão**, **Racional**. O racional explica a regra que justifica a mudança (ex: "só as primeiras linhas do Sobre aparecem antes do 'ver mais'"), para a pessoa poder decidir se concorda.

## 7. Salvar e apresentar

- **Nome do arquivo:** `LinkedIn Review <slug> <YYYY-MM-DD>.md`, onde o slug vem do final da URL (ex: `/in/maria-silva` vira `maria-silva`). Sem URL, use o nome do perfil compartilhado.
- Salve em `outputFolder` (ou `--output`).
- Se já existir relatório do mesmo dia, atualize-o. Se existir relatório de data anterior, crie um novo, leia o mais recente e preencha "Evolução desde a Última Avaliação" (notas anteriores e atuais, sugestões aplicadas e pendentes). Assim a pessoa acompanha o progresso entre rodadas.
- Ao final, mostre no chat só o resumo executivo e o caminho do arquivo, e pergunte se a pessoa quer ajustar tom, foco ou alguma seção. Na primeira execução, diga também onde o perfil e o objetivo foram salvos e como mudá-los.

## Restrições

- Não usar travessão (—); usar hífen (-).
- Não usar `---` como separador de seções no relatório (apenas no frontmatter).
- Não executar nenhuma ação no LinkedIn (editar perfil, enviar DM, conectar). A skill só gera o relatório; enviar mensagens é decisão da pessoa.
- Guardar no perfil compartilhado só caminhos, datas e o objetivo de carreira, nunca o conteúdo do perfil ou do relatório.
- Não fazer `git commit` nem `git push`.

## Exemplo

**Primeira chamada:**

```
/career:linkedin-review
```

A skill pede o link do perfil, o setor, o cargo-alvo e as empresas-alvo, tenta ler o perfil, pede o PDF exportado se o LinkedIn bloquear a leitura, e gera o relatório.

**Rodadas seguintes:**

```
/career:linkedin-review --perfil "C:/Users/ana/Downloads/Profile.pdf"
```

**Resposta final esperada:**

```
Avaliando para Engenharia de Software Sênior em fintech, mirando Nubank e Stone.
Relatório salvo em Documents/Candidaturas/LinkedIn Review ana-souza 2026-10-10.md.
Diagnóstico: título genérico e Sobre em lista de tarefas; experiências fortes, mas sem números no LinkedIn.
Maior impacto: novo título com o cargo-alvo, Sobre em PAS e métricas da trajetória nas 2 experiências mais recentes.
Evolução: Título subiu de 4/10 para 7/10 desde 2026-09-12.
```
