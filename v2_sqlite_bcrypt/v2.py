import sqlite3
import bcrypt

conexao = sqlite3.connect("usuarios.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
    )
""")

conexao.commit()

cursor.execute("DELETE FROM usuarios")
cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'usuarios'")
conexao.commit()

print("===========================")
print("  SISTEMA DE AUTENTICAÇÃO ")
print("===========================")

while True:
    print("[1] CADASTRO")
    print("[2] LOGIN")
    print("[3] SAIR")


    opcao = input('\nSelecione uma das opções acima: ')

    if opcao not in ('1', '2', '3'):
        print('Opção inválida ')
        continue

    if opcao == '1':
        print('---- Cadastro ----')                    
        usuario = input('Digite seu nome de usuário: ')
        senha = input('Digite sua senha: ')

        cursor.execute(                                         
            "SELECT usuario FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        resultado = cursor.fetchone()

        if resultado:
            print('\nUsuário já cadastrado')

        else:
            senha_hash = bcrypt.hashpw(
                senha.encode('utf-8'),
                bcrypt.gensalt()
            )
            
            print("Hash gerado:", senha_hash)

            cursor.execute(
                "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
                (usuario, senha_hash)
             )
            conexao.commit()

            print('\nCadastro realizado com sucesso!')

    elif opcao == '2':
        print('---- Login ----')
        usuario = input('Digite seu nome de usuário cadastrado: ')
        senha = input('Digite sua senha cadastrada: ')

        cursor.execute(
            "SELECT senha FROM usuarios WHERE usuario = ?",
            (usuario,)
        )

        resultado = cursor.fetchone()

        if resultado:
            senha_banco = resultado[0]

            if bcrypt.checkpw(senha.encode('utf-8'), senha_banco):
                print('\nLogin realizado com sucesso!')
                print('\nBem-vindo(a),', usuario)
            else:
                print('Senha incorreta.')
        else:
            print('\nUsuário não encontrado')

    elif opcao == '3':
        print('---- Sair ----')
        break




