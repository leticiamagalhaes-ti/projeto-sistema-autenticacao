import sqlite3
import bcrypt


from fastapi import FastAPI
from pydantic import BaseModel

# 1. Modelo dos dados recebidos
class Usuario(BaseModel):
    usuario: str
    senha: str

# 2. Crio a aplicação
app = FastAPI()

# 3. Rota inicial
@app.get("/") 
def inicio():
    return {"mensagem": "API de autenticação funcionando"}


# 4. Cadastro (endpoints que substituem o menu:)
@app.post("/cadastro")
def cadastro(dados: Usuario):
    #aqui entra a lógica do cadastro da V2 sqlite + bcrypt
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
        )
    """)

    cursor.execute(                                         
        "SELECT usuario FROM usuarios WHERE usuario = ?",
         (dados.usuario,)
      )
    resultado = cursor.fetchone()

    if resultado:
        return {"mensagem": "Usuário já cadastrado"}
    else:
        senha_hash = bcrypt.hashpw(
            dados.senha.encode('utf-8'),
            bcrypt.gensalt()
        )
    
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (dados.usuario, senha_hash)
        )
        conexao.commit()
        conexao.close()

        return {"mensagem": "Cadastro realizado com sucesso!"}

# 5. Login
@app.post("/login")
def login(dados: Usuario):

    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT senha FROM usuarios WHERE usuario = ?",
        (dados.usuario,)
    )
    
    resultado = cursor.fetchone()
    
    if resultado:
         senha = resultado[0]
    
         if bcrypt.checkpw(dados.senha.encode('utf-8'), senha):
            conexao.close()
            return {"mensagem": "Login realizado com sucesso! Bem-vindo(a)!!"}

         else:
            conexao.close()
            return {"mensagem": "Senha incorreta."}
         
    else:
        conexao.close()
        return {"mensagem": "Usuário não encontrado"}