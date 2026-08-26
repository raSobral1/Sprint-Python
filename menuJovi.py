
def pausar():
    # Pausa a tela para o usuario ler a mensagem antes de voltar ao menu.
    input("\nPressione ENTER para voltar ao menu principal...")


def ler_inteiro(mensagem, minimo=None, maximo=None):
    # Le um numero inteiro e valida se ele esta dentro do intervalo permitido.
    while True:
        try:
            numero = int(input(mensagem))

            if minimo is not None and numero < minimo:
                print(f"Digite um numero maior ou igual a {minimo}.")
            elif maximo is not None and numero > maximo:
                print(f"Digite um numero menor ou igual a {maximo}.")
            else:
                return numero

        except ValueError:
            print("Entrada invalida. Digite apenas numeros.")


def mostrar_funcionalidades():
    # Mostra uma explicacao breve sobre as principais funcoes do sistema SLID.
    print("\n=== FUNCOES DO SLID ===")
    print("SLID significa: See, Listen and Identify.")
    print("See: captura imagens do quadro durante a aula.")
    print("Listen: registra falas importantes em tempo real.")
    print("Identify: identifica e resume os pontos principais da aula.")
    print("Galeria: organiza os registros por materia.")


def listar_materias(materias):
    # Exibe todas as materias cadastradas na lista recebida por parametro.
    print("\n=== MATERIAS CADASTRADAS ===")

    if len(materias) == 0:
        print("Nenhuma materia cadastrada.")
        return

    for indice, materia in enumerate(materias):
        print(f"{indice + 1} - {materia['nome']}")


def escolher_materia(materias):
    # Permite o usuario escolher uma materia e retorna a materia selecionada.
    if len(materias) == 0:
        print("Cadastre uma materia antes de usar esta opcao.")
        return None

    listar_materias(materias)
    escolha = ler_inteiro("Escolha o numero da materia: ", 1, len(materias))
    return materias[escolha - 1]


def entrar_no_modo_slid(materias, historico):
    # Simula o uso do SLID, salvando quadro, fala e resumo na materia escolhida.
    print("\n=== MODO SLID ===")
    materia = escolher_materia(materias)

    if materia is None:
        return

    print(f"\nMateria selecionada: {materia['nome']}")
    iniciar = ler_inteiro("Digite 1 para iniciar o SLID ou 0 para cancelar: ", 0, 1)

    if iniciar == 0:
        print("Operacao cancelada.")
        return

    quadro = input("Digite uma breve descricao do que apareceu no quadro: ")
    fala = input("Digite uma fala importante registrada na aula: ")
    resumo = input("Digite o ponto principal identificado pelo SLID: ")

    # Dicionario que representa uma captura feita durante a aula.
    captura = {
        "quadro": quadro,
        "fala": fala,
        "resumo": resumo
    }

    materia["capturas"].append(captura)
    historico.append(f"Captura adicionada na materia {materia['nome']}")

    print("\nSLID ativado com sucesso!")
    print("Registro salvo na galeria da materia.")


def exibir_galeria(materias):
    # Mostra os registros salvos dentro da materia escolhida pelo usuario.
    print("\n=== GALERIA ORGANIZADA ===")
    materia = escolher_materia(materias)

    if materia is None:
        return

    print(f"\nPasta de fotos e registros: {materia['nome']}")

    if len(materia["capturas"]) == 0:
        print("Ainda nao existem registros salvos para esta materia.")
        return

    for indice, captura in enumerate(materia["capturas"]):
        print(f"\nRegistro {indice + 1}")
        print(f"Quadro: {captura['quadro']}")
        print(f"Fala: {captura['fala']}")
        print(f"Resumo: {captura['resumo']}")


def adicionar_materia(materias, historico):
    # Adiciona uma nova materia na lista, evitando nomes vazios ou repetidos.
    print("\n=== ADICIONAR MATERIA ===")
    nome = input("Digite o nome da nova materia: ").strip()

    if nome == "":
        print("O nome da materia nao pode ficar vazio.")
        return

    for materia in materias:
        if materia["nome"].lower() == nome.lower():
            print("Essa materia ja esta cadastrada.")
            return

    nova_materia = {
        "nome": nome,
        "capturas": []
    }

    materias.append(nova_materia)
    historico.append(f"Materia adicionada: {nome}")

    print(f"{nome} foi adicionada com sucesso!")


def remover_materia(materias, historico):
    # Remove uma materia da lista depois de pedir confirmacao ao usuario.
    print("\n=== REMOVER MATERIA ===")
    materia = escolher_materia(materias)

    if materia is None:
        return

    confirmar = ler_inteiro(f"Digite 1 para remover {materia['nome']} ou 0 para cancelar: ", 0, 1)

    if confirmar == 1:
        materias.remove(materia)
        historico.append(f"Materia removida: {materia['nome']}")
        print("Materia removida com sucesso.")
    else:
        print("Operacao cancelada.")


def mostrar_historico(historico):
    # Exibe as acoes realizadas durante o uso do programa.
    print("\n=== HISTORICO DE USO ===")

    if len(historico) == 0:
        print("Nenhuma acao registrada ate o momento.")
        return

    for indice, acao in enumerate(historico):
        print(f"{indice + 1} - {acao}")


def mostrar_desenvolvedores():
    # Mostra os integrantes do grupo e o email de contato do projeto.
    print("\n=== DESENVOLVEDORES ===")
    print("Erick Ripari Gomes")
    print("Fabricio Denig De Avila")
    print("Guilherme Mazzini Nunes Canno")
    print("Luan Schinello Garbin")
    print("Rafael Taboada Sobral")
    print("\n=== CONTATO ===")
    print("Email: projetoslid@gmail.com")


def mostrar_menu(nome_usuario):
    # Exibe as opcoes principais do menu para o usuario.
    print(f"\n=== MENU MODO SLID JOVI | Usuario: {nome_usuario} ===")
    print("1 - Funcionalidades do SLID")
    print("2 - Entrar no modo SLID")
    print("3 - Galeria organizada")
    print("4 - Adicionar nova materia")
    print("5 - Remover materia")
    print("6 - Historico de uso")
    print("7 - Desenvolvedores e contato")
    print("8 - Sair")


def menu():
    # Funcao principal que controla o fluxo do programa.
    # Cada materia e um dicionario com nome e uma lista de capturas.
    materias = [
        {"nome": "Front-end", "capturas": []},
        {"nome": "Calculo", "capturas": []},
        {"nome": "Python", "capturas": []},
        {"nome": "Web Development", "capturas": []}
    ]

    historico = []

    # O strip remove espacos extras digitados antes ou depois do nome.
    nome_usuario = input("Digite seu nome para interagir com o menu: ").strip()

    if nome_usuario == "":
        nome_usuario = "Visitante"

    print(f"Seja bem-vindo(a) ao menu do modo SLID, {nome_usuario}!")

    # While que mantem o programa rodando ate o usuario escolher a opcao de sair.
    while True:
        mostrar_menu(nome_usuario)
        opcao = ler_inteiro("Escolha uma opcao entre 1 e 8: ", 1, 8)

        if opcao == 1:
            mostrar_funcionalidades()
            pausar()
        elif opcao == 2:
            entrar_no_modo_slid(materias, historico)
            pausar()
        elif opcao == 3:
            exibir_galeria(materias)
            pausar()
        elif opcao == 4:
            adicionar_materia(materias, historico)
            pausar()
        elif opcao == 5:
            remover_materia(materias, historico)
            pausar()
        elif opcao == 6:
            mostrar_historico(historico)
            pausar()
        elif opcao == 7:
            mostrar_desenvolvedores()
            pausar()
        elif opcao == 8:
            print("\nFechando o menu...")
            print("Programa encerrado.")
            break

menu()