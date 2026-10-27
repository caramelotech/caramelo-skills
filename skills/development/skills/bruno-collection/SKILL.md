---
name: bruno-collection
description: Cria e mantém collections do Bruno (cliente de API open source) a partir do código de um projeto ou de uma lista de endpoints. Analisa rotas, DTOs, validações e guards para gerar as requisições em YAML (OpenCollection), organiza pastas e ambientes, configura variáveis e autenticação sem expor segredos (tokens e senhas em .env ignorado pelo git ou como variáveis secretas) e sempre documenta as regras de cada endpoint. Por padrão cria tudo em `.bruno/` na raiz do repositório. Use quando for pedido criar, atualizar ou documentar uma collection do Bruno, requisições do Bruno, arquivos .bru ou opencollection.yml, ou "documentar os endpoints no Bruno".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Bruno Collection

Gere uma collection do Bruno pronta para uso por qualquer pessoa do time: cada endpoint do projeto vira uma requisição organizada, documentada com suas regras, parametrizada por variáveis e com a autenticação configurável sem que ninguém precise commitar credenciais.

Antes de escrever arquivos, leia as referências desta skill (caminhos relativos à pasta da skill):

- `references/opencollection-yaml.md` - formato dos arquivos (collection, pasta, requisição, ambiente) com exemplos completos.
- `references/auth-patterns.md` - padrões de autenticação (login com token, API key, Basic, OAuth 2, cookie de sessão) e como guardar cada credencial.
- `references/docs-template.md` - modelos da documentação da collection, das pastas e de cada requisição.

## Preferências

Leia e siga `../../shared/preferences.md` (caminho relativo à pasta desta skill). Esta skill usa `autonomy` e as preferências abaixo, em `skills.bruno-collection` (ou em `repos.<repositório>.bruno-collection`, que têm prioridade):

| Preferência      | Valores                            | Padrão    | O que controla                                                                                                    |
| ---------------- | ---------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------- |
| `secretStrategy` | `dotenv`, `secret-vars`            | `dotenv`  | Onde ficam as credenciais: `.env` ignorado pelo git (funciona no app e no CLI) ou variáveis secretas do app Bruno |
| `environments`   | lista de nomes                     | `local`   | Ambientes criados por padrão (ex: `local`, `staging`)                                                             |
| `collectionPath` | caminho relativo (por repositório) | `.bruno`  | Onde fica a collection no repositório                                                                             |
| `format`         | `yml`, `bru` (por repositório)     | detectado | Formato dos arquivos: `yml` (OpenCollection, padrão do Bruno desde a v3.1) ou `bru` (legado)                      |

Perguntas da configuração inicial (junto com a de autonomia, se faltar):

- **Segredos** (header `Segredos`): `Arquivo .env fora do git` (Recommended), `Variáveis secretas do Bruno`.
- **Ambientes** (header `Ambientes`): `Só local` (Recommended), `Local e staging`, `Local, staging e produção`.

`collectionPath` e `format` não são perguntados: detecte-os (veja "Passo 1") e grave em `repos.<repositório>.bruno-collection` para não detectar de novo.

Flags (têm prioridade sobre as preferências, só nesta chamada): `--reconfigurar` refaz as perguntas de preferências; `--preferencias` mostra as preferências em uso e não executa a tarefa; `--path <caminho>` usa outra pasta para a collection.

## Regras inegociáveis

Valem em qualquer modo de autonomia:

1. **Nenhum segredo real em arquivo versionado.** Senhas, tokens, API keys, client secrets, cookies e dados pessoais nunca aparecem em `opencollection.yml`, `folder.yml`, requisições, ambientes, `.env.sample` nem na documentação. Se encontrar um segredo no código analisado (ex: chave em `config.ts`), não o copie: use uma variável e avise no relatório final que o segredo está exposto no código.
2. **Credenciais sempre por variável.** Toda credencial é referenciada como `{{nome}}`, declarada no ambiente como `{{process.env.NOME}}` (estratégia `dotenv`) ou como `secret: true` sem valor (estratégia `secret-vars`).
3. **Tokens obtidos em tempo de execução ficam em variáveis de runtime** (`bru.setVar`), nunca gravados em arquivo (não use `bru.setEnvVar` com `persist`).
4. **Scripts não registram segredos.** Nada de `console.log` de token, senha, header `Authorization` ou corpo de login.
5. **`.env` sempre no `.gitignore`.** Crie ou atualize `<collectionPath>/.gitignore` e confira que o `.gitignore` da raiz não ignora a pasta da collection inteira.
6. **Toda requisição tem documentação** com as regras do endpoint (veja "Passo 5"). Requisição sem `docs` não está pronta.
7. **Requisições com efeito colateral são sinalizadas** na documentação (o que cria, altera, apaga, envia ou cobra) e endpoints destrutivos não ficam habilitados no ambiente de produção.
8. **Não invente comportamento.** Regra que não está no código nem na spec vira "A confirmar" na documentação, nunca uma suposição apresentada como fato.

## Passo 1 - Entender o pedido e o repositório

1. Identifique o alvo: o repositório atual (padrão), outro caminho informado, uma spec OpenAPI/Swagger, ou uma lista de endpoints colada na conversa.
2. Defina a pasta da collection: `--path`, a preferência `collectionPath` do repositório, ou `.bruno/` na raiz do repositório (raiz do git; sem git, o diretório atual).
   - Um projeto com uma API: a própria `.bruno/` é a raiz da collection (`.bruno/opencollection.yml`).
   - Monorepo com várias APIs independentes: uma collection por API em `.bruno/<nome-da-api>/`, cada uma com seu `opencollection.yml`, ambientes e `.env`.
3. Verifique se já existe uma collection:
   - Em `<collectionPath>` ou em outra pasta do repositório (procure `opencollection.yml` e `bruno.json`). Se existir em outro lugar, use-a e grave esse caminho em `collectionPath`, em vez de criar uma segunda.
   - `opencollection.yml` presente: formato `yml`. Só `bruno.json` com arquivos `.bru`: formato `bru`; mantenha `.bru` e sugira a migração para YAML no relatório final (o próprio app Bruno faz a migração), sem migrar por conta própria.
   - Collection nova: use `yml`.
4. Com collection existente, trabalhe de forma incremental: adicione o que falta, atualize o que mudou no código e preserve o que a pessoa editou à mão (nomes, exemplos, scripts, ordem). Nunca renumere `seq` de requisições existentes.

## Passo 2 - Levantar os endpoints

Use a fonte mais confiável disponível, nesta ordem:

1. **Spec OpenAPI/Swagger** do projeto (`openapi.yaml`, `swagger.json`, rota `/docs-json`, decorators que geram a spec). Use-a como base e confira contra o código.
2. **Código das rotas.** Localize pelo framework:

   | Stack               | Onde procurar                                                                                 |
   | ------------------- | --------------------------------------------------------------------------------------------- |
   | NestJS              | `@Controller`, `@Get/@Post/...`, DTOs com `class-validator`, `@UseGuards`, `@Roles`, pipes    |
   | Express / Fastify   | `router.get(...)`, `app.post(...)`, `fastify.route`, middlewares, schemas Zod/Joi/JSON Schema |
   | Next.js             | `app/**/route.ts` (handlers `GET`, `POST`...), `pages/api/**`, `middleware.ts`                |
   | FastAPI / Flask     | `@app.get`, `APIRouter`, modelos Pydantic, `Depends(...)`, `@blueprint.route`                 |
   | Django / DRF        | `urls.py`, `ViewSet`, `serializers.py`, `permission_classes`                                  |
   | Spring              | `@RestController`, `@RequestMapping`, `@Valid` + Bean Validation, `@PreAuthorize`             |
   | ASP.NET             | `[ApiController]`, `[Route]`, `[HttpGet]`, `[Authorize]`, DataAnnotations                     |
   | Go (gin, echo, chi) | `r.GET(...)`, `e.POST(...)`, structs com tags `binding`/`validate`, middlewares               |
   | Rails / Laravel     | `config/routes.rb`, `routes/api.php`, Form Requests, policies                                 |

3. **Lista informada pela pessoa.** Complete o que faltar perguntando (no modo `assistido`) ou marcando como "A confirmar" (no modo `autonomo`).

Para cada endpoint, registre: método, caminho, parâmetros de caminho e de query, headers exigidos, corpo (campos, tipos, obrigatórios, validações e limites), autenticação e permissões (papéis, escopos, dono do recurso), respostas e códigos de status (sucesso e erros), efeitos colaterais (escrita em banco, e-mail, fila, webhook, cobrança), idempotência, paginação, rate limit e regras de negócio relevantes. Ignore rotas internas de infraestrutura (health checks de orquestrador, métricas) a menos que a pessoa peça, e liste-as no relatório como ignoradas.

Pedido grande (mais de ~30 endpoints)? No modo `assistido`, mostre o inventário agrupado e confirme o escopo antes de escrever. No modo `autonomo`, gere tudo.

## Passo 3 - Planejar a estrutura

```
.bruno/
├── opencollection.yml        # raiz: nome, auth e headers padrão, docs da collection
├── .gitignore                # ignora .env e variações
├── .env.sample               # nomes das variáveis de segredo, sem valores
├── README.md                 # como configurar e usar a collection
├── environments/
│   ├── local.yml
│   └── staging.yml
├── auth/
│   ├── folder.yml
│   └── login.yml
└── users/
    ├── folder.yml
    ├── list-users.yml
    ├── get-user.yml
    └── create-user.yml
```

- **Pastas por recurso ou domínio** (`users`, `orders`, `payments`), espelhando os controllers/módulos do projeto. Uma pasta `auth/` primeiro quando houver login. Subpastas só quando o recurso tiver sub-recursos claros (`orders/items`).
- **Nomes de arquivo** em kebab-case e em inglês, no formato verbo + recurso (`list-users.yml`, `create-order.yml`). O `info.name` é legível e em inglês, combinando com o arquivo (`List Users`). Nome de arquivo, `info.name` e intenção da requisição devem concordar.
- **`seq`** define a ordem no app e no runner: comece em 1 e use intervalos (1, 2, 3...) dentro de cada pasta, na ordem de uso natural: login, listar, buscar, criar, atualizar, apagar. Ao inserir requisições em collection existente, use o próximo número livre, sem renumerar as demais.
- **Tags** (`info.tags`) para recortes úteis no runner: `smoke` para leituras seguras, `write` para requisições com efeito colateral, `destructive` para remoções.

## Passo 4 - Variáveis e ambientes

Escolha o escopo de cada variável pelo uso, do mais amplo para o mais restrito (a precedência do Bruno é a inversa: runtime > requisição > pasta > ambiente > collection > global):

| Escopo     | Onde fica                                  | Use para                                                                                               |
| ---------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Ambiente   | `environments/<nome>.yml`                  | O que muda entre ambientes: `baseUrl`, credenciais (via `process.env` ou `secret: true`), IDs de teste |
| Collection | `opencollection.yml` (`request.variables`) | Constantes iguais em todos os ambientes: `apiVersion`, `contentType`                                   |
| Pasta      | `folder.yml` (`request.variables`)         | Valores compartilhados por um recurso: prefixo de caminho, ID de exemplo                               |
| Requisição | `runtime.variables` da requisição          | Valores usados só naquela requisição                                                                   |
| Runtime    | memória, via `bru.setVar`                  | Valores obtidos durante a execução: `accessToken`, `createdUserId`                                     |
| Processo   | `.env` na raiz da collection               | Segredos lidos como `{{process.env.NOME}}`                                                             |

Regras:

- **Host sempre em variável**: toda URL começa com `{{baseUrl}}`; nunca escreva um host fixo em requisição. Se a API tiver prefixo (`/api/v1`), inclua-o no `baseUrl` ou numa variável de collection, de forma consistente.
- **Nomes em camelCase e em inglês** (`baseUrl`, `accessToken`, `userEmail`); no `.env`, em `UPPER_SNAKE_CASE` com um prefixo do projeto quando houver risco de colisão (`MYAPI_USER_PASSWORD`).
- **Toda variável de ambiente tem `description`** dizendo o que é, de onde vem e se é segredo.
- **Um arquivo por ambiente**, com as mesmas variáveis em todos (só os valores mudam). Ambiente de produção, se pedido, tem `color` vermelha e não habilita requisições destrutivas.
- **Segredos** conforme `secretStrategy`:
  - `dotenv` (padrão): no ambiente, `value: '{{process.env.MYAPI_USER_PASSWORD}}'`; o valor real vai em `<collectionPath>/.env` (criado pela pessoa a partir do `.env.sample`). Funciona no app e no `bru` CLI.
  - `secret-vars`: no ambiente, `- secret: true` com `name` e `description`, sem `value`. A pessoa preenche no app Bruno, que guarda o valor criptografado na máquina dela. No CLI, o valor vai por `--env-var nome=valor`.
- **Valores obtidos na execução** (token, ID criado) ficam em runtime: `bru.setVar("createdUserId", res.body.id)` no script `after-response`, ou com uma action `set-variable`.
- Para dados que a pessoa deve digitar na hora e nunca guardar (código de MFA, OTP), use variável de prompt: `{{?MFA code}}`.

## Passo 5 - Documentação

Sempre gere três níveis, seguindo `references/docs-template.md`:

1. **`README.md` da collection** (`<collectionPath>/README.md`): o que a collection cobre, pré-requisitos, como abrir no Bruno, como criar o `.env` a partir do `.env.sample` ou preencher as variáveis secretas, como selecionar o ambiente, como autenticar, como rodar pelo CLI e uma tabela com todas as variáveis.
2. **`docs` da collection e de cada pasta** (`opencollection.yml` e `folder.yml`): visão geral, regras comuns (autenticação, paginação, formato de erro, rate limit) e a ordem de uso.
3. **`docs` de cada requisição**: descrição, autenticação e permissões, parâmetros e corpo com tipos, obrigatoriedade e validações, regras de negócio, respostas e erros, efeitos colaterais e idempotência, e dependências (de qual requisição vem cada variável).

Escreva a documentação no idioma predominante do projeto (README, comentários). Na dúvida, em português.

## Passo 6 - Autenticação

Quando a API exigir autenticação, siga `references/auth-patterns.md`:

1. Identifique o mecanismo no código (guards, middlewares, decorators, filtros de segurança) e as rotas públicas.
2. Configure a auth **uma vez, no nível mais alto possível** (`opencollection.yml` ou `folder.yml`) e use `auth: inherit` nas requisições. Rotas públicas (login, cadastro, health) omitem `auth`.
3. Para fluxos de login, crie a requisição em `auth/` que lê as credenciais das variáveis de ambiente e grava o token com `bru.setVar` no `after-response`. Se o token expira, documente o tempo de vida e como renovar (requisição de refresh ou rodar o login de novo).
4. Documente os passos no `README.md` (seção "Autenticação") e no `docs` da pasta `auth/`: o que preencher, em que ordem rodar, onde o token fica e por quanto tempo vale.
5. Para OAuth 2, prefira a auth nativa do Bruno (`type: oauth2`) com `clientId`/`clientSecret` vindos de variáveis.

## Passo 7 - Scripts, asserções e testes

- **Asserções** (`runtime.assertions`) para checagens declarativas simples: `res.status eq 200`, `res.body.id isDefined`.
- **Script `tests`** em toda requisição: primeiro o status esperado, depois a invariante principal da resposta (formato do corpo, campo obrigatório, contrato). Não faça testes frágeis sobre valores que mudam.
- **Script `before-request`** só quando necessário: gerar chave de idempotência, assinar requisição (HMAC), montar valores derivados. Ao ler segredo em script, falhe com mensagem clara se ele estiver vazio, sem mostrar o valor:

  ```javascript
  const secret = bru.getEnvVar("webhookSecret");
  if (!secret) {
    throw new Error(
      "webhookSecret is not set. See .bruno/README.md#authentication",
    );
  }
  ```

- **Script `after-response`** para capturar valores em runtime (`bru.setVar`).
- Requisições de escrita usam dados de exemplo claramente fictícios (`jane.doe@example.com`), nunca dados reais encontrados no projeto.

## Passo 8 - Gravar e validar

- No modo `assistido`, mostre a árvore de arquivos e o inventário de endpoints e confirme antes de escrever. No modo `autonomo`, escreva direto.
- Nunca sobrescreva um arquivo da collection que não foi criado nesta execução sem preservar as edições existentes; ao atualizar, edite só os campos necessários.
- Valide o resultado:
  - Todo YAML é válido e segue `references/opencollection-yaml.md` (campos com os nomes exatos; o Bruno ignora ou rejeita campos desconhecidos).
  - Toda `{{variavel}}` usada está declarada em algum escopo, ou é preenchida em runtime por uma requisição documentada como dependência.
  - Nenhum segredo literal: procure por padrões como `Bearer ey`, `password:`, `apiKey:`, `sk_`, `-----BEGIN` nos arquivos gerados.
  - `.env` está ignorado (`git check-ignore <collectionPath>/.env`).
  - Se o `bru` CLI estiver instalado e a API estiver rodando localmente, ofereça rodar as leituras seguras: `bru run --env local --tags smoke` a partir da pasta da collection. Não rode requisições de escrita sem confirmação.

## Relatório final

Informe, em poucas linhas:

- Onde a collection foi criada ou atualizada e quantas requisições por pasta.
- Endpoints ignorados e o motivo; regras marcadas como "A confirmar".
- O que a pessoa precisa fazer para usar: criar o `.env` a partir do `.env.sample` (ou preencher as variáveis secretas), selecionar o ambiente, rodar o login.
- Segredos encontrados expostos no código do projeto, se houver.
- Na primeira execução, onde as preferências foram salvas e como mudá-las.

Não faça commit: a pessoa decide quando versionar a collection.

## Variáveis

| Variável             | Descrição                                  | Exemplo          |
| -------------------- | ------------------------------------------ | ---------------- |
| `{{alvo}}`           | Projeto, pasta, spec ou lista de endpoints | `./apps/api`     |
| `{{collectionPath}}` | Pasta da collection                        | `.bruno`         |
| `{{ambientes}}`      | Ambientes a criar                          | `local, staging` |

## Exemplo

**Input:**

```
Crie a collection do Bruno para a API deste repositório.
```

```typescript
// src/users/users.controller.ts
@Controller("users")
@UseGuards(JwtAuthGuard)
export class UsersController {
  @Get(":id")
  findOne(@Param("id", ParseUUIDPipe) id: string) {
    return this.usersService.findOne(id);
  }
}
```

**Output esperado** (`.bruno/users/get-user.yml`):

```yaml
info:
  name: Get User
  type: http
  seq: 2
  tags:
    - smoke

http:
  method: GET
  url: "{{baseUrl}}/users/{{userId}}"
  auth: inherit

runtime:
  assertions:
    - expression: res.status
      operator: eq
      value: "200"
  scripts:
    - type: tests
      code: |-
        test("returns the requested user", () => {
          expect(res.status).to.equal(200);
          expect(res.body).to.have.property("id", bru.getEnvVar("userId"));
        });

settings:
  encodeUrl: true

docs: |-
  # Get User

  Returns a single user by id.

  ## Auth
  Bearer token (JWT). Run `auth/login` first.

  ## Path params
  | Name | Type | Required | Rules |
  | ---- | ---- | -------- | ----- |
  | `id` | uuid | yes | Must be a valid UUID (`ParseUUIDPipe`), otherwise 400 |

  ## Responses
  | Status | When |
  | ------ | ---- |
  | 200 | User found |
  | 400 | `id` is not a UUID |
  | 401 | Missing or invalid token |
  | 404 | User does not exist (to confirm: not visible in the controller) |

  ## Side effects
  None (read only).
```

## Notas

- O Bruno guarda a collection como arquivos no repositório: ela é versionada junto com o código e revisada em PR. Trate mudanças de endpoint e de collection na mesma alteração.
- O app Bruno também importa specs OpenAPI, Postman e Insomnia. Esta skill gera a collection a partir do código para incluir as regras e a autenticação que a importação não captura.
- GraphQL, gRPC e WebSocket seguem a mesma organização; consulte a seção correspondente em `references/opencollection-yaml.md` e mantenha cada collection num único formato.
- Combina com `development:owasp-check` quando a análise dos endpoints revelar rotas sem autenticação ou validação: registre o achado na documentação e sugira a revisão de segurança.
