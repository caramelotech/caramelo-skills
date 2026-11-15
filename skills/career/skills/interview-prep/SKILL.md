---
name: interview-prep
description: Organiza os dados de uma candidatura de emprego (vaga, tecnologias exigidas, nível, domínio) numa nota e prepara a pessoa para a entrevista, cruzando a descrição da vaga (texto ou URL) com a trajetória profissional dela - prováveis perguntas técnicas e comportamentais, pontos fortes para destacar, lacunas para se preparar e perguntas para fazer à pessoa entrevistadora. No primeiro uso coleta onde está a trajetória (arquivo, currículo, LinkedIn ou outro link, ou ajuda a criá-la se a pessoa não tiver), onde salvar e o idioma, e guarda no perfil de carreira compartilhado; depois só a vaga é necessária. Use quando a pessoa quiser registrar uma candidatura, se preparar para uma entrevista ou entender o quanto o perfil bate com uma vaga.
allowed-tools:
  - Read(~/.claude/plugins/**/caramelo-skills/**)
  - Read(~/.claude/career/profile.json)
  - Edit(~/.claude/career/profile.json)
  - Skill
  - AskUserQuestion
---

# Preparação de candidatura

Organiza os dados de uma vaga numa nota de candidatura e prepara quem está se candidatando para a entrevista, cruzando a descrição da vaga com a trajetória profissional da pessoa. Não escreve texto de candidatura pronto para envio: isso é papel da `application-text` (que roda esta preparação por baixo) e da `cover-letter`.

## Parâmetros

| Parâmetro        | Flag           | Obrigatório | O que é                                                                                    |
| ---------------- | -------------- | ----------- | ------------------------------------------------------------------------------------------ |
| `<vaga>`         | `--vaga`       | Sim         | Descrição da vaga: texto colado, caminho de arquivo ou URL                                 |
| `[empresa]`      | `--empresa`    | Não         | Nome da empresa. Se não vier, é extraído da vaga                                           |
| `[processo]`     | `--processo`   | Não         | Informações sobre o processo seletivo (etapas, formato da entrevista, quem vai entrevistar) |
| `[trajetoria]`   | `--trajetoria` | Não         | Caminho da trajetória. Sobrescreve o perfil só nesta chamada                               |
| `[output]`       | `--output`     | Não         | Pasta da nota. Sobrescreve o perfil só nesta chamada                                       |
| `[idioma]`       | `--idioma`     | Não         | Idioma da nota. Sobrescreve o perfil só nesta chamada                                      |
| `--reconfigurar` | -              | Não         | Refaz a configuração inicial do perfil                                                     |

Se a skill for chamada sem a vaga, peça só a vaga em uma mensagem de chat e aguarde.

## 1. Perfil

Leia e siga `../../shared/profile.md` (caminho relativo à pasta desta skill). Esta skill usa os campos `name`, `careerSource`, `extraSources`, `outputFolder`, `language` e `noteStyle`, e não tem perguntas próprias de configuração.

Se o arquivo compartilhado não puder ser lido, use `~/.claude/career/profile.json` diretamente e pergunte só a trajetória e a pasta de destino que faltarem.

## 2. Receber a vaga

Siga "Receber a vaga" do perfil compartilhado.

## 3. Verificar candidatura existente

Procure em `outputFolder` uma nota `Candidatura <Empresa>.md` (ou `Candidatura <Empresa> <Cargo>.md`) da mesma vaga.

- Se existir, a chamada é uma atualização: releia a análise já feita e atualize só o que mudou (por exemplo, refazer a preparação depois de novas informações em `--processo`), sem recriar a nota.
- Preserve seções adicionadas por outras skills, como `## Texto da Candidatura` (da `application-text`).
- Se não existir, siga normalmente.

## 4. Ler a trajetória

Siga "Ler a trajetória" do perfil compartilhado. Leia também as `extraSources` que tratarem de tecnologias, domínios ou responsabilidades citados na vaga, como registros de entrevistas anteriores.

## 5. Analisar a vaga

Identifique:

- **Tecnologias exigidas e desejáveis** (linguagens, frameworks, bancos, infraestrutura)
- **Domínio de negócio** (fintech, saúde, e-commerce, etc.)
- **Nível** (júnior, pleno, sênior, liderança)
- **Responsabilidades principais**
- **Diferenciais valorizados** (testes, observabilidade, comunicação, liderança, etc.)
- **Modelo de trabalho** (remoto, híbrido, presencial), se informado

## 6. Preparar o material de entrevista

Cruzando a análise da vaga com a trajetória, monte:

- **Prováveis perguntas técnicas:** ligadas às tecnologias e responsabilidades da vaga. Separe o que a trajetória mostra que a pessoa já enfrentou de verdade (perguntas que ela responde com exemplo real) do que é território novo (perguntas para estudar antes).
- **Prováveis perguntas comportamentais:** ligadas ao nível e aos diferenciais valorizados (trabalho em equipe, ambiguidade, priorização, feedback, liderança, etc.).
- **Pontos fortes para destacar:** experiências concretas da trajetória que respondem a um requisito da vaga. Para cada uma, cite a experiência e o requisito que ela cobre, não apenas "tenho experiência com X".
- **Lacunas e como abordá-las:** requisitos que a trajetória não cobre. Sugira como responder com honestidade (experiência adjacente, disposição real para aprender). Nunca sugira inflar ou inventar experiência.
- **Perguntas para fazer à pessoa entrevistadora:** 3 a 5 perguntas específicas da vaga e da empresa, sobre o time, o produto, os desafios técnicos citados na vaga ou critérios de sucesso no papel. Nada genérico como "quais os desafios do time?" solto.

Se vier `--processo`, adapte o material às etapas informadas (por exemplo, mais peso em system design se houver essa etapa).

## 7. Salvar ou atualizar a nota

Nome do arquivo: `Candidatura <Empresa>.md` (veja "Nome dos arquivos" no perfil compartilhado). Escreva no idioma do perfil (ou de `--idioma`).

```markdown
---
company: "<Empresa>"
position: <Título da vaga>
created: <YYYY-MM-DD>
tags:
  - candidatura
  - <principais tecnologias da vaga>
---

# Candidatura <Empresa> - <Título da vaga>

## Sobre a Vaga

- [<Título da vaga> | <Empresa>](<URL da vaga, se houver>)
- **Nível:** <nível>
- **Domínio:** <domínio>
- **Modelo de trabalho:** <se informado>
- <Outros pontos relevantes: produto ou área, benefícios notáveis, requisitos incomuns>

## Tecnologias e Requisitos

- **Obrigatórios:** <lista resumida>
- **Desejáveis:** <lista resumida>

## Preparação para Entrevista

### Prováveis Perguntas Técnicas

- <pergunta> - <se a trajetória já cobre com exemplo real ou é ponto a estudar>

### Prováveis Perguntas Comportamentais

- <pergunta>

### Pontos Fortes para Destacar

- <experiência da trajetória> - cobre o requisito <requisito da vaga>

### Lacunas e Como Abordá-las

- <requisito não coberto> - <como responder com honestidade>

### Perguntas para Fazer à Pessoa Entrevistadora

- <pergunta específica da vaga ou empresa>
```

- Com `noteStyle` igual a `obsidian`, siga "Notas de candidatura no estilo obsidian" do perfil compartilhado. Com `md`, use o modelo acima como está.
- Se a vaga veio como texto (sem URL), mantenha só o título e a empresa no primeiro item.
- Não use `---` como separador no corpo da nota (apenas no frontmatter).

## 8. Resposta final

Mostre um resumo curto: os principais pontos da análise da vaga e 1 ou 2 destaques de cada parte da preparação, sem repetir a nota inteira. Informe o caminho da nota e pergunte se a pessoa quer aprofundar algum ponto. Na primeira execução, diga também onde o perfil foi salvo e como mudá-lo.

## Restrições

- Nome, empregadores, tecnologias e diferenciais vêm sempre da trajetória informada, nunca de suposições.
- Nas lacunas, nunca sugerir mentir ou inflar experiência, só como enquadrar com honestidade o que existe.
- Não escrever texto de candidatura pronto para envio.
- Não usar travessão (—); usar hífen (-).
- Não enviar candidaturas, preencher formulários nem publicar nada em nome da pessoa.
- Não fazer `git commit` nem `git push`.

## Exemplo

**Input:**

```
/career:interview-prep https://empresa.exemplo/vagas/backend-senior --processo "Entrevista técnica com live coding e etapa de system design"
```

**Resposta final esperada:**

```
Nota salva em Documents/Candidaturas/Candidatura Acme.md.
Vaga sênior de backend em fintech, com Java, Spring Boot e Kafka obrigatórios.
Ponto forte: a migração de pagamentos para eventos na experiência atual cobre o requisito de mensageria.
Lacuna: Kubernetes não aparece na trajetória; a nota sugere como falar da experiência com Docker e ECS.
Quer aprofundar alguma parte, como a etapa de system design?
```
