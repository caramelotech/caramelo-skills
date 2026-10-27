# Formato OpenCollection YAML

Referência dos arquivos que o Bruno lê no formato YAML (OpenCollection 1.0.0), padrão para collections novas desde o Bruno 3.1. Use exatamente estes nomes de campo: o formato é validado por schema e campos desconhecidos são rejeitados ou ignorados.

## Arquivos da collection

| Arquivo                    | Papel                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| `opencollection.yml`       | Raiz da collection: nome, defaults de requisição (auth, headers, variáveis, scripts) e docs |
| `<pasta>/folder.yml`       | Configuração da pasta: nome, ordem, defaults e docs                                         |
| `<pasta>/<requisicao>.yml` | Uma requisição por arquivo                                                                  |
| `environments/<nome>.yml`  | Um ambiente por arquivo                                                                     |
| `.env`                     | Segredos lidos como `{{process.env.NOME}}` (nunca versionado)                               |

## `opencollection.yml`

```yaml
opencollection: "1.0.0"

info:
  name: Acme API
  summary: HTTP API for the Acme platform
  version: "1.0.0"

request:
  auth:
    type: bearer
    token: "{{accessToken}}"
  headers:
    - name: Accept
      value: application/json
  variables:
    - name: apiVersion
      value: v1
      description: API version prefix used in every path
  scripts:
    - type: tests
      code: |-
        test("responds in under 2s", () => {
          expect(res.getResponseTime()).to.be.below(2000);
        });

docs:
  type: text/markdown
  content: |-
    # Acme API

    See README.md for setup.

bundled: false

extensions:
  bruno:
    ignore:
      - node_modules
      - .git
```

- `request` define os defaults herdados por todas as pastas e requisições (`auth`, `headers`, `variables`, `scripts`, `settings`).
- `docs` aceita uma string Markdown ou o objeto `{ type, content }`.
- `extensions.bruno.ignore` lista pastas que o Bruno não deve ler.

## `folder.yml`

```yaml
info:
  name: Users
  type: folder
  seq: 2

request:
  auth: inherit
  variables:
    - name: userId
      value: 00000000-0000-0000-0000-000000000001
      description: Example user id used by get/update/delete requests

docs: |-
  # Users

  CRUD of platform users. Requires a bearer token (run `auth/login` first).
```

## Requisição HTTP

```yaml
info:
  name: Create User
  type: http
  seq: 3
  tags:
    - write
  description: Creates a user

http:
  method: POST
  url: "{{baseUrl}}/users"
  headers:
    - name: Idempotency-Key
      value: "{{idempotencyKey}}"
      description: Same key on retries of the same operation
  params:
    - name: notify
      value: "false"
      type: query
      description: Send welcome e-mail
      disabled: true
  body:
    type: json
    data: |-
      {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "role": "member"
      }
  auth: inherit

runtime:
  variables:
    - name: idempotencyKey
      value: ""
  assertions:
    - expression: res.status
      operator: eq
      value: "201"
    - expression: res.body.id
      operator: isDefined
  actions:
    - type: set-variable
      phase: after-response
      selector:
        expression: res.body.id
        method: jsonq
      variable:
        name: createdUserId
        scope: runtime
  scripts:
    - type: before-request
      code: |-
        const { v4: uuidv4 } = require("uuid");
        if (!bru.getVar("idempotencyKey")) {
          bru.setVar("idempotencyKey", uuidv4());
        }
    - type: tests
      code: |-
        test("creates the user", () => {
          expect(res.status).to.equal(201);
          expect(res.body).to.have.property("id");
          expect(res.body.email).to.equal("jane.doe@example.com");
        });

settings:
  encodeUrl: true
  timeout: 0
  followRedirects: true

docs: |-
  # Create User
  ...
```

### Campos

- `info`: `name`, `type` (`http`), `seq`, `tags`, `description`.
- `http`: `method`, `url`, `headers[]` (`name`, `value`, `description`, `disabled`), `params[]` (`name`, `value`, `type`: `query` ou `path`, `description`, `disabled`), `body`, `auth`.
- Parâmetros de caminho: use `:id` na URL e declare em `params` com `type: path`, ou interpole uma variável (`/users/{{userId}}`). Escolha um estilo e mantenha na collection toda.
- `auth`: um objeto de auth (veja abaixo), `inherit` para herdar da pasta/collection, ou omita o campo para "sem autenticação".
- `runtime`: `variables[]`, `assertions[]`, `actions[]`, `scripts[]`.
- `settings`: `encodeUrl`, `timeout` (ms, `0` sem limite), `followRedirects`, `maxRedirects`.
- `docs`: string Markdown.

### Corpo (`http.body`)

```yaml
# JSON, text, XML
body:
  type: json        # json | text | xml | sparql
  data: |-
    { "name": "Jane" }

# application/x-www-form-urlencoded
body:
  type: form-urlencoded
  data:
    - name: grant_type
      value: password

# multipart/form-data
body:
  type: multipart-form
  data:
    - name: description
      type: text
      value: Profile picture
    - name: file
      type: file
      value: ./fixtures/avatar.png
```

### Asserções

`expression` (ex: `res.status`, `res.body.items.length`, `res.headers['content-type']`), `operator` e `value` (string). Operadores comuns: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `in`, `notIn`, `contains`, `notContains`, `length`, `matches`, `notMatches`, `startsWith`, `endsWith`, `isEmpty`, `isNotEmpty`, `isNull`, `isDefined`, `isUndefined`, `isTruthy`, `isFalsy`, `isJson`, `isNumber`, `isString`, `isBoolean`, `isArray`.

### Scripts

`runtime.scripts[]` com `type` igual a `before-request`, `after-response` ou `tests`, e `code`. APIs mais usadas:

| API                                                                | Uso                                         |
| ------------------------------------------------------------------ | ------------------------------------------- |
| `bru.getEnvVar(name)`                                              | Lê variável do ambiente ativo               |
| `bru.getProcessEnv(name)`                                          | Lê variável do `.env`                       |
| `bru.getVar(name)` / `bru.setVar(name, value)`                     | Lê e grava variável de runtime (em memória) |
| `bru.getCollectionVar`, `bru.getFolderVar`, `bru.getRequestVar`    | Lê variáveis de cada escopo                 |
| `bru.interpolate(str)`                                             | Resolve `{{...}}` numa string               |
| `req.setHeader(name, value)`, `req.getBody()`, `req.setBody(body)` | Altera a requisição antes do envio          |
| `res.status`, `res.body`, `res.headers`, `res.getResponseTime()`   | Lê a resposta                               |
| `test(name, fn)` + `expect(...)` (Chai)                            | Testes                                      |

Em scripts, sempre falhe com `throw new Error(...)` quando um valor obrigatório estiver ausente, sem imprimir o valor.

### Variáveis tipadas

Valores são strings por padrão. Para número, booleano ou objeto:

```yaml
variables:
  - name: pageSize
    value:
      type: number
      data: "20"
```

## Ambiente (`environments/<nome>.yml`)

```yaml
name: local
color: "#22c55e"
variables:
  - name: baseUrl
    value: http://localhost:3000/api
    description: API base URL, including the global prefix
  - name: userEmail
    value: "{{process.env.ACME_USER_EMAIL}}"
    description: Login e-mail of a test user. Set it in .bruno/.env
  - name: userPassword
    value: "{{process.env.ACME_USER_PASSWORD}}"
    description: Password of the test user. Secret, set it in .bruno/.env
  - secret: true
    name: adminApiKey
    description: Admin API key. Secret, fill it in Bruno (Environment > Secrets)
```

- Variável comum: `name`, `value`, `description`, `disabled`.
- Variável secreta: `secret: true`, `name`, `description` e opcionalmente `type`. **Nunca** tem `value`: o Bruno guarda o valor criptografado na máquina de cada pessoa.
- `extends: <outro-ambiente>` herda as variáveis de outro ambiente (útil para `staging` estender um `base`).
- Nomes com ponto no `.env` usam colchetes: `{{process.env['acme.token']}}`.

## `.env`, `.env.sample` e `.gitignore`

`.env` (local, nunca versionado):

```bash
ACME_USER_EMAIL=dev@example.com
ACME_USER_PASSWORD="P@ss#word"
```

Valores com `#`, aspas, barra invertida ou quebra de linha vão entre aspas (sem aspas, `ABC#DEF` vira `ABC`).

`.env.sample` (versionado, sem valores):

```bash
# Copy to .env and fill in. Never commit .env.
ACME_USER_EMAIL=
ACME_USER_PASSWORD=
```

`.gitignore` da collection:

```gitignore
.env
.env.*
!.env.sample
```

## CLI (`@usebruno/cli`)

```bash
npm install -g @usebruno/cli
cd .bruno
bru run --env local                          # toda a collection
bru run users --env local                    # uma pasta
bru run --env local --tags smoke             # só as tags informadas
bru run --env local --exclude-tags destructive
bru run --env staging --env-var adminApiKey="$ADMIN_API_KEY"   # variável secreta no CI
bru run --env local --reporter-junit results.xml
```

O CLI carrega o `.env` da raiz da collection automaticamente. Variáveis `secret: true` não chegam ao CLI: passe-as com `--env-var`.

## Outros tipos de requisição

GraphQL, gRPC e WebSocket usam `info.type` igual a `graphql`, `grpc` e `websocket`, com seções próprias em `http`/`grpc`/`websocket`. Ao gerar um desses tipos, confira o formato num arquivo criado pelo próprio app Bruno (crie a requisição no app e leia o arquivo) antes de replicar. Os scripts de gRPC usam os tipos `grpc:before-call-start`, `grpc:after-call-end`, `grpc:before-message-send` e `grpc:after-message-receive`, e os arquivos `.proto` são registrados em `config.protobuf` do `opencollection.yml`.

## Formato legado `.bru`

Collections antigas usam `bruno.json` + `collection.bru` + arquivos `.bru`. Se a collection existente estiver nesse formato, mantenha `.bru` nos arquivos novos (não misture formatos sem migrar) e sugira a migração pelo app Bruno. Equivalências principais: `meta { name, type, seq }`, `get|post|... { url, body, auth }`, `headers { }`, `body:json { }`, `auth:bearer { token }`, `vars:pre-request { }`, `assert { }`, `script:pre-request { }`, `script:post-response { }`, `tests { }`, `docs { }`; nos ambientes, `vars { }` e `vars:secret [ nome ]`.
