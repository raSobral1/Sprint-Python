def retornaMenu():
    sair = int(input("===Digite qualquer número para retornar ao menu===: "))
    if sair >= 0:
         menu()
    if sair < 0:
        print("Digite um número válido")  

def funcionalidades():
        print("=== FUNÇÕES SLID ===")
        print("See, Listen and Identify")
        print("See: Vê, captura o quadro apenas com a camera ativada")
        print("Listen: Escuta, registra a fala em tempo real")
        print("Identify: Identifica, destasca o essencial da aula")
        retornaMenu()

def entraNoModo():
    print("Bem-vido(a) ao modo SLID!")
    iniciar = int(input("Digite 1 para iniciar ou 0 para voltar ao menu: "))
    if iniciar == 1:
            print("Para começar a usar o modo SLID, coloque a camera apontada para o quadro para iniciar as funcoes")
            print("SLID ativado e operando")
            entraNoModo()
    elif iniciar == 0:
        menu()
    else:
        print("Escolha um número válido ")
        entraNoModo()

materias = ["Front-end ", "Cálculo", "Python", "Web-Development"]

def galeriaOrganizada():
    
    for i in range(len(materias)):
        print(f"{i} - {materias[i]}")

    escolha = int(input("Escolha o número da matéria para entrar na pasta: "))

    if escolha >= 0 and escolha < len(materias):
        print(f"Você entrou na Pasta de fotos da matéria: {materias[escolha]}!")

    else:
        print("Escolha um número válido")
        galeriaOrganizada()
    
    retornaMenu()
        
def adicionaGaleria():

    novaMateria = input("Digite o nome da nova matéria: ")

    materias.append(novaMateria)

    print(f"{novaMateria} foi adicionada com sucesso!")

    retornaMenu()
   
def desenvolvedores():
    print("===Desenvolvedores===")
    print("Erick RIpari Gomes")
    print("Fabricio Denig De Avila")
    print("Guilherme Mazzini Nunes Canno")
    print("Luan Schinello Garbin")
    print("Rafael Taboada Sobral")
    print("===CONTADO===")
    print("Email para entrar em contato: projetoslid@gmail.com")
    retornaMenu()
    
def iniciar():
    nome = input("Digite seu nome para ter interação com o menu: ")
    print(f"Seja Bem-vido(a) ao menu do modo SLID {nome}! ")

iniciar()

def menu():
    opcao = 0
    while True:

        print("=== MENU MODO SLID JOVI ===")
        print("1 - Funcionalidades do SLID")
        print("2 - Entrar no modo SLID")
        print("3 - Galeria Organizada")
        print("4 - Adicionar nova Matéria na Galeria")
        print("5 - Desenvolvedores do SLID e Contado")
        print("6 - Sair do menu" )

        opcao = int(input("Escolha as opções entre 1 a 6: "))

        if opcao == 1:
            funcionalidades()
        
        elif opcao == 2:
            entraNoModo()
        
        elif opcao == 3:
            galeriaOrganizada()
        
        elif opcao == 4:
            adicionaGaleria()
        
        elif opcao == 5:
            desenvolvedores()
        
        elif opcao == 6:
            print("Fechando o menu...")
            print("Programa encerado")
            break
        
        else:
            print("Escolha um número válido ")

menu()


