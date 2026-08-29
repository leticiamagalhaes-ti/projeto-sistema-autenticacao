print("===========================")
print("  SISTEMA DE AUTENTICAÇÃO ")
print("===========================")

usuarios = {}

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
        
        if usuario in usuarios:
            print("\nUsuário já cadastrado")
        else:
            usuarios[usuario] = senha 
            print('\nCadastro realizado com sucesso!')

    elif opcao == '2':
        print('---- Login ----')
        usuario = input('Digite seu nome de usuário cadastrado: ')
        senha = input('Digite sua senha cadastrada: ')

        if usuario in usuarios and usuarios[usuario] == senha:
            print('\nLogin realizado com sucesso!')
            print('Bem-vindo(a),', usuario)
        else:
            print('Usuário ou senha incorretos.')


    elif opcao == '3':
        print('---- Sair ----')
        break
