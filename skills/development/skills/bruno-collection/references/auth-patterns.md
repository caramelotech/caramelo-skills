# Padrões de autenticação

Como configurar cada mecanismo de autenticação na collection sem expor credenciais. Em todos eles:

- A auth é declarada uma vez em `opencollection.yml` (ou no `folder.yml` da pasta que precisa dela) e as requisições usam `auth: inherit`.
- Rotas públicas omitem `auth` (sem autenticação).
- Credenciais de longa duração (senha, API key, client secret) vêm do ambiente, que as lê de `.env` (`{{process.env.NOME}}`) ou de uma variável `secret: true`.
- Tokens obtidos na execução ficam em runtime (`bru.setVar`) e somem ao fechar o app.

## Como descobrir o mecanismo no código

| Sinal no código                                                                | Mecanismo provável       |
| ------------------------------------------------------------------------------ | ------------------------ |
| `JwtAuthGuard`, `passport-jwt`, `jsonwebtoken.verify`, `Authorization: Bearer` | Bearer com login próprio |
| `x-api-key`, `apiKey` em header ou query, `ApiKeyGuard`                        | API key                  |
| `passport-http`, `basicAuth`, `WWW-Authenticate: Basic`                        | Basic                    |
| `/oauth/token`, `client_credentials`, Keycloak, Auth0, Cognito, Entra ID       | OAuth 2                  |
| `express-session`, `Set-Cookie` no login, `cookie-parser`, CSRF token          | Sessão por cookie        |
| Assinatura HMAC de corpo/headers, `X-Signature`, webhooks                      | Requisição assinada      |

Registre também: rotas públicas, papéis/escopos exigidos por rota, tempo de vida do token, endpoint de refresh e logout.

## Bearer com login próprio (padrão mais comum)

Ambiente:

```yaml
variables:
  - name: baseUrl
    value: http://localhost:3000
  - name: userEmail
    value: "{{process.env.ACME_USER_EMAIL}}"
    description: Login e-mail. Set ACME_USER_EMAIL in .bruno/.env
  - name: userPassword
    value: "{{process.env.ACME_USER_PASSWORD}}"
    description: Login password. Secret, set ACME_USER_PASSWORD in .bruno/.env
```

`opencollection.yml`:

```yaml
request:
  auth:
    type: bearer
    token: "{{accessToken}}"
```

`auth/login.yml` (sem `auth`, porque é pública):

```yaml
info:
  name: Login
  type: http
  seq: 1

http:
  method: POST
  url: "{{baseUrl}}/auth/login"
  body:
    type: json
    data: |-
      {
        "email": "{{userEmail}}",
        "password": "{{userPassword}}"
      }

runtime:
  scripts:
    - type: before-request
      code: |-
        if (!bru.getEnvVar("userEmail") || !bru.getEnvVar("userPassword")) {
          throw new Error("Login credentials are not set. Copy .bruno/.env.sample to .bruno/.env and fill it in.");
        }
    - type: after-response
      code: |-
        if (res.status === 200 || res.status === 201) {
          bru.setVar("accessToken", res.body.accessToken);
          if (res.body.refreshToken) {
            bru.setVar("refreshToken", res.body.refreshToken);
          }
        }
    - type: tests
      code: |-
        test("returns an access token", () => {
          expect(res.status).to.be.oneOf([200, 201]);
          expect(res.body.accessToken).to.be.a("string").and.not.empty;
        });

docs: |-
  # Login
  ...
```

Ajuste os nomes dos campos (`accessToken`, `token`, `access_token`) ao contrato real da API.

Variações:

- **Token automático antes de cada requisição**: se a pessoa preferir não rodar o login à mão, coloque um script `before-request` na collection que chama o login com `bru.sendRequest` quando `accessToken` estiver vazio. Documente que isso faz uma chamada extra de login.
- **Refresh**: crie `auth/refresh-token.yml` usando `{{refreshToken}}` e atualizando `accessToken` no `after-response`. Documente quando usar (token expira em X minutos).
- **Vários perfis** (admin e usuário comum): variáveis separadas (`adminEmail`, `memberEmail`), uma requisição de login por perfil e tokens separados (`adminAccessToken`), com a auth da pasta de administração apontando para o token certo.

## API key

```yaml
# environments/local.yml
variables:
  - name: apiKey
    value: "{{process.env.ACME_API_KEY}}"
    description: API key of a test account. Secret, set ACME_API_KEY in .bruno/.env

# opencollection.yml
request:
  auth:
    type: apikey
    key: x-api-key
    value: "{{apiKey}}"
    placement: header # header | query
```

## Basic

```yaml
request:
  auth:
    type: basic
    username: "{{basicUser}}"
    password: "{{basicPassword}}"
```

`basicUser` e `basicPassword` no ambiente, lidos do `.env`.

## OAuth 2

Prefira a auth nativa do Bruno, que busca e renova o token sozinha.

Client credentials (máquina a máquina):

```yaml
request:
  auth:
    type: oauth2
    flow: client_credentials
    accessTokenUrl: "{{authUrl}}/oauth/token"
    credentials:
      clientId: "{{clientId}}"
      clientSecret: "{{clientSecret}}"
      placement: basic_auth_header # basic_auth_header | body
    scope: read:users write:users
    tokenConfig:
      placement:
        header: Authorization
    settings:
      autoFetchToken: true
      autoRefreshToken: true
```

Authorization code (login no navegador), com PKCE:

```yaml
request:
  auth:
    type: oauth2
    flow: authorization_code
    authorizationUrl: "{{authUrl}}/authorize"
    accessTokenUrl: "{{authUrl}}/oauth/token"
    callbackUrl: http://localhost:8080/callback
    credentials:
      clientId: "{{clientId}}"
      clientSecret: "{{clientSecret}}"
      placement: body
    scope: openid profile email
    pkce:
      method: S256
    settings:
      autoFetchToken: true
      autoRefreshToken: true
```

Outros fluxos: `resource_owner_password_credentials` (com `resourceOwner.username`/`password` vindos de variáveis) e `implicit`. `clientSecret` sempre por variável; nunca use o client de produção em ambientes de teste.

## Sessão por cookie

O Bruno guarda e reenvia cookies automaticamente entre requisições da mesma collection. Crie `auth/login.yml` com as credenciais do ambiente e documente que as demais requisições dependem do cookie gerado. Se a API exigir token CSRF, capture-o no `after-response` do login (`bru.setVar("csrfToken", res.headers["x-csrf-token"])`) e envie como header nas requisições de escrita (`X-CSRF-Token: {{csrfToken}}`), declarado no `folder.yml`.

## Requisição assinada (HMAC, webhooks)

Gere a assinatura num script `before-request`, lendo o segredo do ambiente e falhando se ele faltar. Assine o corpo exatamente como será enviado.

```javascript
const CryptoJS = require("crypto-js");

const secret = bru.getEnvVar("webhookSecret");
if (!secret) {
  throw new Error(
    "webhookSecret is not set. See .bruno/README.md#authentication",
  );
}

const body = JSON.stringify(req.getBody());
req.setBody(body);
const signature = CryptoJS.HmacSHA256(body, secret).toString(CryptoJS.enc.Hex);
req.setHeader("X-Signature", `sha256=${signature}`);
```

Nunca imprima a assinatura nem o segredo.

## Estratégia `secret-vars`

Quando a preferência for usar variáveis secretas do app em vez de `.env`, troque a declaração no ambiente:

```yaml
variables:
  - secret: true
    name: userPassword
    description: Login password. Fill it in Bruno (Environment settings > Secrets)
```

O valor fica criptografado na máquina de cada pessoa e não vai para o arquivo. No CLI e no CI, passe com `bru run --env staging --env-var userPassword="$ACME_USER_PASSWORD"`. Documente essa diferença no `README.md`.

## O que documentar sobre autenticação

No `README.md` da collection (seção "Autenticação") e no `docs` da pasta `auth/`:

1. Qual mecanismo a API usa e quais rotas são públicas.
2. Quais variáveis preencher, onde (`.env` ou aba de segredos do Bruno) e como obter os valores (ex: "peça um usuário de teste ao time", "crie um client no Keycloak de dev").
3. A ordem de uso: selecionar o ambiente, rodar `auth/login`, depois as demais.
4. Onde o token fica (variável de runtime `accessToken`), quanto tempo vale e como renovar.
5. Papéis e permissões: qual perfil é necessário para cada pasta.
6. Avisos de segurança: nunca commitar `.env`, nunca usar credenciais de produção pessoais, revogar credenciais expostas.
