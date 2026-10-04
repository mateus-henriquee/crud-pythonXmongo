# ====== IMPORTS ======
import os # lê variáveis de ambiente.
from urllib.parse import quote_plus # escapa caracteres especiais da senha (@, :, /).

from bson import ObjectId # tipo do _id do Mongo
from bson.errors import InvalidId # erro quando o ID é malformado.
from dotenv import load_dotenv # carrega o arquivo .env.
from pymongo import MongoClient # faz a conexão.


# ====== CONFIGURAÇÃO ======
load_dotenv() # copia o conteúdo do .env para o ambiente.

USUARIO = os.getenv("MONGODB_USERNAME", "")
SENHA = os.getenv("MONGODB_PASSWORD", "")
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
# "os.getenv("X", padrão)" lê a variável. Se não existir, usa o padrão.

# Se a URI tiver placeholders, troca pelas credenciais (com escape).
for marcador in ("<db_username>", "<username>"):
    MONGO_URI = MONGO_URI.replace(marcador, quote_plus(USUARIO))
for marcador in ("<db_password>", "<password>"):
    MONGO_URI = MONGO_URI.replace(marcador, quote_plus(SENHA))


# ====== CONEXÃO ======
client = MongoClient(MONGO_URI)
db = client["meu_banco"]
usuarios = db["usuarios"]
usuarios.create_index("email", unique=True)


# ====== CRUD ======
# ---------- CREATE ----------
def criar(nome: str, email: str, idade: int) -> str:
    resultado = usuarios.insert_one({"nome": nome, "email": email, "idade": idade})
    return str(resultado.inserted_id)


# ---------- READ ----------
def listar(filtro: dict | None = None) -> list[dict]:
    return list(usuarios.find(filtro or {}))


def buscar_por_id(id_: str) -> dict | None:
    try:
        return usuarios.find_one({"_id": ObjectId(id_)})
    except InvalidId:
        return None


# ---------- UPDATE ----------
def atualizar(id_: str, **campos) -> bool:
    try:
        r = usuarios.update_one({"_id": ObjectId(id_)}, {"$set": campos})
    except InvalidId:
        return False
    return r.matched_count > 0


# ---------- DELETE ----------
def deletar(id_: str) -> bool:
    try:
        r = usuarios.delete_one({"_id": ObjectId(id_)})
    except InvalidId:
        return False
    return r.deleted_count > 0


# ---------- MENU ----------
def mostrar(u: dict) -> None:
    print(f"{u['_id']} | {u['nome']} | {u['email']} | {u['idade']} anos")


def menu() -> None:
    while True:
        print("\n1) Criar  2) Listar  3) Buscar  4) Atualizar  5) Deletar  0) Sair")
        op = input("> ").strip()

        if op == "1":
            try:
                id_ = criar(input("Nome: "), input("Email: "), int(input("Idade: ")))
                print("Criado:", id_)
            except ValueError:
                print("Idade inválida.")
            except Exception as e:
                print("Erro:", e)

        elif op == "2":
            for u in listar():
                mostrar(u)

        elif op == "3":
            u = buscar_por_id(input("ID: "))
            mostrar(u) if u else print("Não encontrado.")

        elif op == "4":
            id_ = input("ID: ")
            campos = {}
            nome = input("Novo nome (enter pula): ")
            email = input("Novo email (enter pula): ")
            idade = input("Nova idade (enter pula): ")
            if nome:
                campos["nome"] = nome
            if email:
                campos["email"] = email
            if idade.isdigit():
                campos["idade"] = int(idade)
            if not campos:
                print("Nada para atualizar.")
            else:
                print("Atualizado." if atualizar(id_, **campos) else "Não encontrado.")

        elif op == "5":
            print("Deletado." if deletar(input("ID: ")) else "Não encontrado.")

        elif op == "0":
            break

# ====== EXECUÇÃO ======
if __name__ == "__main__":
    menu()