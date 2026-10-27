# Modelos de documentação

Toda collection gerada tem três níveis de documentação. Adapte os títulos ao idioma do projeto e remova seções que não se aplicam (exceto "Regras" e "Respostas", que sempre existem). Quando uma informação não estiver no código nem na spec, escreva "A confirmar" em vez de supor.

## 1. `README.md` da collection

```markdown
# <Nome da API> - Collection do Bruno

Requisições da <API> para desenvolvimento e testes manuais. Cobre <N> endpoints em <pastas>.

## Pré-requisitos

- [Bruno](https://www.usebruno.com/) 3.1 ou superior
- API rodando localmente (`<comando para subir a API>`) ou acesso ao ambiente de staging

## Configuração

1. Abra o Bruno e use **Open Collection** apontando para a pasta `.bruno/`.
2. Copie `.bruno/.env.sample` para `.bruno/.env` e preencha os valores (veja a tabela de variáveis).
   O `.env` está no `.gitignore` e nunca deve ser commitado.
3. Selecione o ambiente (`local` ou `staging`) no canto superior direito.

## Autenticação

<Mecanismo (ex: JWT Bearer). Rotas públicas: <lista>.>

1. Preencha `ACME_USER_EMAIL` e `ACME_USER_PASSWORD` no `.env` com um usuário de teste (<como obter>).
2. Rode `auth/Login`. O token fica na variável de runtime `accessToken` e vale por <tempo>.
3. As demais requisições herdam o token automaticamente. Se receber 401, rode o login de novo.

<Perfis e permissões, se houver: qual usuário usar para cada pasta.>

## Variáveis

| Variável      | Escopo   | Segredo | Origem                     | Descrição                  |
| ------------- | -------- | ------- | -------------------------- | -------------------------- |
| `baseUrl`     | Ambiente | Não     | `environments/*.yml`       | URL base da API            |
| `userEmail`   | Ambiente | Sim     | `.env` (`ACME_USER_EMAIL`) | E-mail do usuário de teste |
| `accessToken` | Runtime  | Sim     | `auth/Login`               | Token JWT da sessão        |

## Rodando pelo CLI

    npm install -g @usebruno/cli
    cd .bruno
    bru run --env local --tags smoke

## Convenções

- Uma pasta por recurso; nomes de arquivo `verbo-recurso.yml`.
- Tags: `smoke` (leituras seguras), `write` (cria ou altera dados), `destructive` (apaga dados).
- Não rode a collection inteira contra staging ou produção: requisições `write` e `destructive` têm efeitos reais.

## Manutenção

Ao criar ou alterar um endpoint, atualize a requisição correspondente no mesmo PR.
```

## 2. `docs` da collection e das pastas

Collection (`opencollection.yml`):

```markdown
# <Nome da API>

<Uma frase sobre o propósito da API.>

## Regras gerais

- Formato: JSON (`Content-Type: application/json`)
- Autenticação: <mecanismo>, configurada na collection; rotas públicas: <lista>
- Paginação: <ex: `?page` (1..n) e `?limit` (máx. 100); resposta com `meta.total`>
- Erros: <formato padrão, ex: `{ "statusCode", "message", "error" }`>
- Rate limit: <ex: 100 req/min por IP; 429 quando exceder> | A confirmar
- Datas: <ex: ISO 8601 em UTC>

## Ordem de uso

1. `auth/Login`
2. <fluxo principal, ex: criar usuário > criar pedido > pagar pedido>
```

Pasta (`folder.yml`):

```markdown
# <Recurso>

<O que o recurso representa e como se relaciona com os outros.>

## Regras do recurso

- Permissão: <ex: leitura para qualquer usuário autenticado; escrita só `admin`>
- <Regras de negócio comuns, ex: e-mail é único; usuário removido é soft delete>

## Variáveis desta pasta

- `userId`: id de exemplo; é atualizado por `Create User` (`createdUserId`)
```

## 3. `docs` de cada requisição

```markdown
# <Nome da requisição>

<O que faz, em uma ou duas frases.>

## Autenticação

<Herdada (Bearer). Papel exigido: `admin`.> | Pública.

## Parâmetros de caminho

| Nome | Tipo | Obrigatório | Regras                 |
| ---- | ---- | ----------- | ---------------------- |
| `id` | uuid | sim         | UUID válido, senão 400 |

## Query

| Nome    | Tipo | Padrão | Regras  |
| ------- | ---- | ------ | ------- |
| `page`  | int  | 1      | >= 1    |
| `limit` | int  | 20     | 1 a 100 |

## Corpo

| Campo   | Tipo   | Obrigatório | Regras                                                      |
| ------- | ------ | ----------- | ----------------------------------------------------------- |
| `name`  | string | sim         | 2 a 100 caracteres                                          |
| `email` | string | sim         | e-mail válido; único (409 se já existir)                    |
| `role`  | enum   | não         | `member` (padrão) ou `admin`; só `admin` pode criar `admin` |

## Regras de negócio

- <ex: o e-mail é normalizado para minúsculas antes de salvar>
- <ex: envia e-mail de boas-vindas quando `notify=true`>

## Respostas

| Status | Quando                                       |
| ------ | -------------------------------------------- |
| 201    | Criado; retorna o usuário sem `password`     |
| 400    | Corpo inválido (lista de erros em `message`) |
| 401    | Sem token ou token inválido                  |
| 403    | Papel insuficiente                           |
| 409    | E-mail já cadastrado                         |

## Efeitos colaterais

<Cria registro em `users`; publica `user.created` na fila; envia e-mail.> | Nenhum (somente leitura).

## Idempotência

<Use `Idempotency-Key`; a mesma chave com o mesmo corpo retorna o resultado original.> | Não idempotente: cada envio cria um novo registro.

## Dependências

- `accessToken`: de `auth/Login`
- Grava `createdUserId` (runtime), usado por `Update User` e `Delete User`
```

## Checklist da documentação

- [ ] Toda requisição tem `docs` com autenticação, regras de entrada, respostas e efeitos colaterais.
- [ ] Validações vêm do código (DTO, schema, pipes) e citam os limites reais.
- [ ] Erros listam os códigos que o código realmente retorna, inclusive os de guards e filtros globais.
- [ ] Requisições `write` e `destructive` dizem o que alteram.
- [ ] Nenhum segredo, token ou dado pessoal real aparece em exemplos.
- [ ] O que não pôde ser confirmado está marcado como "A confirmar".
