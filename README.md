# CRUD Python x MongoDB

CRUD de usuários em Python com MongoDB Atlas. Interface por menu no terminal.

## Funcionalidades

- Criar usuário
- Listar usuários
- Buscar por ID
- Atualizar usuário
- Deletar usuário
- Email único (índice no MongoDB)

## Tecnologias

- Python 3.10+
- [PyMongo](https://pymongo.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- MongoDB Atlas

## Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd crud-pythonXmongo
```

2. Instale as dependências:

```bash
pip install pymongo dnspython python-dotenv
```

3. Crie um arquivo `.env` na raiz do projeto:

```dotenv
MONGODB_USERNAME=seu_usuario
MONGODB_PASSWORD=sua_senha
MONGODB_URI=mongodb+srv://<db_username>:<db_password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

> Mantenha `<db_username>` e `<db_password>` na URI. O script os substitui pelos valores acima.

## Configuração do MongoDB Atlas

1. Crie um cluster gratuito (M0).
2. Em **Database Access**, crie um usuário com a role **Read and write to any database**.
3. Em **Network Access**, libere o seu IP.
4. Em **Connect → Drivers → Python**, copie a string de conexão para o `.env`.

## Uso

```bash
python crud_mongo.py
```

Menu:

```
1) Criar  2) Listar  3) Buscar  4) Atualizar  5) Deletar  0) Sair
```

## Estrutura dos dados

Banco: `meu_banco` | Coleção: `usuarios`

```json
{
  "_id": "ObjectId",
  "nome": "Ana",
  "email": "ana@email.com",
  "idade": 30
}
```

## Segurança

O arquivo `.env` contém credenciais. Não envie para o repositório. Ele deve estar no `.gitignore`:

```
.env
__pycache__/
```

## Erros comuns

| Erro | Causa |
|------|-------|
| `Authentication failed` | Usuário ou senha incorretos |
| `ServerSelectionTimeoutError` | IP não liberado no Atlas |
| `DuplicateKeyError` | Email já cadastrado |
