---
name: cover-letter
description: Gera uma carta de apresentação completa para candidatura de emprego (formato de carta, para e-mail, LinkedIn ou anexo de currículo) a partir da descrição da vaga (texto ou URL) e da trajetória profissional da pessoa. No primeiro uso, coleta onde está a trajetória (arquivo, currículo, LinkedIn ou outro link, ou ajuda a criá-la se a pessoa não tiver), o formato de saída, onde salvar e o idioma, e guarda no perfil de carreira compartilhado com as outras skills da categoria para não perguntar de novo; a partir daí só a vaga é necessária. Use quando a pessoa pedir carta de apresentação, cover letter, carta para candidatura ou texto de apresentação para uma vaga.
allowed-tools:
  - Read(~/.claude/plugins/**/caramelo-skills/**)
  - Read(~/.claude/career/profile.json)
  - Edit(~/.claude/career/profile.json)
  - Skill
  - AskUserQuestion
---

# Carta de apresentação

Cria uma carta de apresentação para uma vaga de emprego, no formato de carta (saudação, corpo, despedida), ancorada na trajetória profissional real da pessoa e nos requisitos da vaga.

A skill é genérica: não assume nada sobre a pessoa. No primeiro uso ela monta um perfil de preferências (seção 1). Nas chamadas seguintes, só pede o que é específico da candidatura: a vaga.

## Parâmetros

| Parâmetro        | Flag           | Obrigatório | O que é                                                                                                    |
| ---------------- | -------------- | ----------- | ---------------------------------------------------------------------------------------------------------- |
| `<vaga>`         | `--vaga`       | Sim         | Descrição da vaga: texto colado, caminho de arquivo ou URL                                                 |
| `[empresa]`      | `--empresa`    | Não         | Nome da empresa. Se não vier, é extraído da vaga                                                           |
| `[trajetoria]`   | `--trajetoria` | Não         | Caminho de arquivo ou pasta com a trajetória profissional. Sobrescreve o perfil só nesta chamada           |
| `[output]`       | `--output`     | Não         | Pasta onde salvar a carta. Sobrescreve o perfil só nesta chamada                                           |
| `[formato]`      | `--formato`    | Não         | `note`, `docx`, `pdf` ou `chat` (seção 6). Sobrescreve o perfil só nesta chamada                           |
| `[idioma]`       | `--idioma`     | Não         | Idioma da carta (ex: `pt-BR`, `en`). Sobrescreve o perfil só nesta chamada; útil para vagas internacionais |
| `[foco]`         | `--foco`       | Não         | Texto livre: o que enfatizar, tom, tamanho, pessoa destinatária                                            |
| `--reconfigurar` | -              | Não         | Refaz a configuração inicial (seção 1) mesmo com perfil salvo                                              |

Se a skill for chamada sem a vaga, peça só a vaga em uma mensagem de chat e aguarde.

## 1. Perfil

Leia e siga `../../shared/profile.md` (caminho relativo à pasta desta skill). O perfil é compartilhado com as outras skills de carreira (`interview-prep`, `application-text`): quem já configurou uma delas não responde de novo o que já está salvo.

Esta skill usa os campos `name`, `careerSource`, `extraSources`, `outputFolder`, `language`, `noteStyle` e `coverLetterFormat`. Quando `coverLetterFormat` faltar, inclua esta pergunta na mesma chamada da `AskUserQuestion` da configuração inicial:

- **Formato da carta** (header `Formato`): `Arquivo de nota (.md)` (Recommended), `Word (.docx)`, `PDF`, `Só no chat`. Valores salvos: `note`, `docx`, `pdf`, `chat`.

Se o arquivo compartilhado não puder ser lido, use `~/.claude/career/profile.json` diretamente e pergunte só a trajetória, a pasta de destino e o formato que faltarem.

## 2. Receber a vaga

Siga "Receber a vaga" do perfil compartilhado.

## 3. Verificar material existente da candidatura

Procure em `outputFolder` arquivos que mencionem a mesma empresa no nome (por exemplo, `Candidatura <Empresa>.md`, `Carta Apresentação <Empresa>.md`, notas de entrevista).

- Se houver análise da vaga, reaproveite-a (nível, domínio, tecnologias obrigatórias e desejáveis, link) para manter consistência entre os textos enviados para a mesma vaga.
- Se já houver carta para a mesma vaga, trate a chamada como nova rodada de ajustes e atualize esse arquivo em vez de criar outro.

## 4. Ler a trajetória e analisar a vaga

1. Siga "Ler a trajetória" do perfil compartilhado.
2. Se houver nota de candidatura reaproveitável (passo 3), use a análise dela. Caso contrário, analise a vaga e liste internamente:
   - **Tecnologias e ferramentas exigidas**
   - **Domínio de negócio** (fintech, saúde, e-commerce, etc.)
   - **Nível** (júnior, pleno, sênior, liderança)
   - **Responsabilidades principais**
   - **Diferenciais valorizados** (testes, observabilidade, comunicação, etc.)
3. Cruze as duas listas: quais requisitos a trajetória comprova, com qual experiência. Requisitos sem evidência na trajetória não entram na carta como experiência.

## 5. Escrever a carta

Escreva no idioma do perfil (ou de `--idioma`), em formato de carta, com 3 a 5 parágrafos (cerca de 250 a 450 palavras, salvo pedido diferente em `--foco`). Estrutura:

1. **Saudação:** sem marcar gênero quando a pessoa destinatária não for conhecida. Em português: `Prezada equipe de recrutamento da <Empresa>,` ou `Prezados,`. Em inglês: `Dear <Empresa> Hiring Team,`.
2. **Abertura:** cargo pretendido e o que motiva a candidatura a essa vaga e empresa especificamente, não algo genérico.
3. **Corpo (1 a 2 parágrafos):** a experiência mais relevante para a vaga, usando os termos exatos das tecnologias da descrição. Ancore o texto na experiência atual e traga experiências passadas que atendam diretamente a um requisito específico.
4. **Diferencial:** um parágrafo sobre o diferencial de carreira, quando ele for relevante para o que a vaga valoriza.
5. **Fechamento:** disponibilidade para conversar, agradecimento e despedida (`Atenciosamente,` ou `Best regards,`) seguida do nome do perfil.

Regras de conteúdo:

- Texto corrido, sem bullet points, como uma carta real.
- Nunca inventar experiências, tecnologias, empresas, números ou resultados que não estejam na trajetória.
- Evitar formulações genéricas como "profissional apaixonado" ou "sou alguém que ama tecnologia".
- Ser neutro quanto ao gênero na escrita sobre a própria pessoa, quando possível ("minha trajetória", "atuo como"), a menos que o perfil ou `--foco` peça outra coisa.
- Tom profissional, mas humano: não soar como currículo em lista.
- Não usar travessão (—); usar hífen (-).

## 6. Apresentar e salvar

Exiba a carta completa no chat e pergunte se a pessoa quer ajustes (tom, foco, ênfase em alguma tecnologia, tamanho, algum trecho). Salve já na primeira apresentação e atualize o mesmo arquivo a cada rodada de ajustes.

Nome do arquivo: `Carta Apresentação <Empresa>` (Title Case, ou `Cover Letter <Empresa>` se a carta for em inglês). Se já existir carta para outra vaga da mesma empresa, inclua o cargo: `Carta Apresentação <Empresa> <Cargo>`. Siga "Nome dos arquivos" do perfil compartilhado.

Por formato (`coverLetterFormat` ou `--formato`):

| Formato | O que gerar                                                                                                                                                                                                                      |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chat`  | Só a carta no chat. Nada é salvo                                                                                                                                                                                                 |
| `note`  | `.md` com o modelo abaixo. Com `noteStyle` igual a `obsidian`, siga "Notas de candidatura no estilo obsidian" do perfil compartilhado; com `md`, use o modelo como está                                                          |
| `docx`  | Só a carta (saudação, corpo, despedida), sem metadados. Use a skill de Word disponível (por exemplo, `anthropic-skills:docx`) ou `pandoc` a partir de um `.md` temporário. Se nenhuma estiver disponível, salve em `.md` e avise |
| `pdf`   | Igual ao `docx`, convertendo para PDF com a skill de PDF disponível ou `pandoc`. Se não for possível, salve em `.md` e avise                                                                                                     |

Modelo Markdown:

```markdown
---
company: "<Empresa>"
position: <Título da vaga>
created: <YYYY-MM-DD>
tags:
  - carta-apresentacao
  - <principais tecnologias da vaga>
---

# Carta de Apresentação - <Empresa> - <Título da vaga>

## Sobre a vaga

- [<Título da vaga> | <Empresa>](<URL da vaga, se houver>)
- **Nível:** <nível>
- **Domínio:** <domínio>

## Carta

<carta completa, com saudação e despedida, em parágrafos>
```

Se a vaga veio como texto (sem URL), mantenha só o título e a empresa no primeiro item. Não use `---` como separador no corpo do arquivo (apenas no frontmatter).

## 7. Resposta final

Depois da carta, responda em 2 a 4 linhas: caminho do arquivo salvo (ou "não salva, formato chat"), requisitos da vaga que a trajetória não comprova e por isso ficaram de fora, e qualquer suposição feita (empresa, cargo, idioma). Na primeira execução, diga também onde o perfil foi salvo e como mudá-lo.

## Restrições

- Nome, empregadores, tecnologias e diferenciais vêm sempre da trajetória informada, nunca de suposições.
- Não incluir dados pessoais sensíveis (documentos, endereço completo, salário) na carta, a menos que a pessoa peça.
- Não enviar a carta, preencher formulários de candidatura nem publicar nada em nome da pessoa.
- Não fazer `git commit` nem `git push`.

## Exemplo

**Primeira chamada (sem perfil):**

```
/career:cover-letter https://empresa.exemplo/vagas/backend-senior
```

A skill faz a configuração inicial (trajetória, destino, idioma e formato da carta), grava `~/.claude/career/profile.json` e gera a carta.

**Chamadas seguintes:**

```
/career:cover-letter --empresa Acme "Buscamos pessoa desenvolvedora backend sênior com Java, Spring Boot e Kafka..."
```

**Resposta final esperada:**

```
Carta salva em Documents/Candidaturas/Carta Apresentação Acme.md.
Kafka não aparece na trajetória e ficou fora da carta como experiência.
Cargo inferido da vaga: Desenvolvedor Backend Sênior.
```

## Notas

- A skill não guarda o conteúdo da trajetória no perfil, só o caminho: atualize o arquivo de trajetória e as próximas cartas já usam a versão nova.
- Para vagas em outro idioma, `--idioma en` gera a carta em inglês sem mudar o perfil.
- Se a vaga já tiver nota da `interview-prep` ou da `application-text`, a carta reaproveita a análise dela para manter os textos consistentes.
- Combina com skills de humanização de texto (como `writing:text-humanizer`) para uma revisão final de estilo.
