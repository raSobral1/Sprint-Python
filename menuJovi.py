import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# Caminho fixo ao lado deste programa, mesmo executando por outra pasta.
ARQUIVO_DADOS = Path(__file__).resolve().with_name("dados_slid.json")
URL_API = "https://pt.wikipedia.org/w/api.php"


def criar_dados_iniciais():
    return {
        "materias": [
            {"nome": nome, "capturas": [], "pesquisas": []}
            for nome in ("Front-end", "Calculo", "Python", "Web Development")
        ],
        "historico": []
    }


def validar_dados(dados):
    # Valida o JSON antes de usar os dados recebidos de um arquivo externo.
    if not isinstance(dados, dict):
        return False
    materias = dados.get("materias")
    historico = dados.get("historico")
    if not isinstance(materias, list) or not isinstance(historico, list):
        return False
    if not all(isinstance(acao, str) for acao in historico):
        return False

    nomes = set()
    for materia in materias:
        if not isinstance(materia, dict):
            return False
        nome = materia.get("nome")
        if not isinstance(nome, str) or not nome.strip() or nome.strip().casefold() in nomes:
            return False
        nomes.add(nome.strip().casefold())
        for lista, campos in (
            ("capturas", ("quadro", "fala", "resumo")),
            ("pesquisas", ("titulo", "resumo", "url"))
        ):
            registros = materia.get(lista)
            if not isinstance(registros, list):
                return False
            for registro in registros:
                if not isinstance(registro, dict):
                    return False
                if not all(isinstance(registro.get(campo), str)
                           and registro[campo].strip() for campo in campos):
                    return False
    return True


def carregar_dados(caminho=ARQUIVO_DADOS):
    # Na primeira execucao, usa as materias iniciais; depois, le o JSON.
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if not validar_dados(dados):
            raise ValueError("Estrutura de dados invalida.")
        return dados
    except FileNotFoundError:
        return criar_dados_iniciais()
    except (OSError, ValueError, UnicodeError) as erro:
        print(f"Nao foi possivel carregar {caminho.name}: {erro}")
        print("Verifique o arquivo antes de abrir novamente. Ele nao foi alterado.")
        return None


def salvar_dados(materias, historico, caminho=ARQUIVO_DADOS):
    # O JSON tambem permite integracao: outro sistema pode ler as mesmas listas.
    dados = {"materias": materias, "historico": historico}
    temporario = caminho.with_suffix(".tmp")
    try:
        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        # Substitui o arquivo anterior somente quando a escrita terminou.
        temporario.replace(caminho)
        return True
    except OSError as erro:
        print(f"Nao foi possivel salvar os dados: {erro}")
        print("As alteracoes continuam apenas na memoria. Tente salvar ao sair.")
        return False


def ler_texto(mensagem):
    # Reutilizada nos campos obrigatorios para impedir registros em branco.
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Este campo nao pode ficar vazio.")


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
    print("Nesta versao academica, quadro, fala e resumo sao digitados manualmente.")
    print("Pesquisa de apoio: consulta resumos na Wikipedia e salva na galeria.")
    print("Materias, registros, pesquisas e historico sao salvos em dados_slid.json.")


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

    quadro = ler_texto("Digite uma breve descricao do que apareceu no quadro: ")
    fala = ler_texto("Digite uma fala importante registrada na aula: ")
    resumo = ler_texto("Digite o ponto principal identificado pelo SLID: ")

    # Dicionario que representa uma captura feita durante a aula.
    captura = {
        "quadro": quadro,
        "fala": fala,
        "resumo": resumo
    }

    materia["capturas"].append(captura)
    historico.append(f"Captura adicionada na materia {materia['nome']}")

    print("\nSLID ativado com sucesso!")
    print("Registro adicionado a galeria da materia.")


def exibir_galeria(materias):
    # Mostra os registros salvos dentro da materia escolhida pelo usuario.
    print("\n=== GALERIA ORGANIZADA ===")
    materia = escolher_materia(materias)

    if materia is None:
        return

    print(f"\nPasta de fotos e registros: {materia['nome']}")

    if not materia["capturas"] and not materia["pesquisas"]:
        print("Ainda nao existem registros salvos para esta materia.")
        return

    for indice, captura in enumerate(materia["capturas"]):
        print(f"\nRegistro {indice + 1}")
        print(f"Quadro: {captura['quadro']}")
        print(f"Fala: {captura['fala']}")
        print(f"Resumo: {captura['resumo']}")

    for indice, pesquisa in enumerate(materia["pesquisas"], start=1):
        print(f"\nPesquisa de apoio {indice}: {pesquisa['titulo']}")
        print(f"Resumo: {pesquisa['resumo']}")
        print(f"Fonte: {pesquisa['url']}")


def buscar_resumo(termo):
    # Consulta real a API publica da Wikipedia, usando somente bibliotecas padrao.
    parametros = {
        "action": "query", "format": "json", "formatversion": 2,
        "generator": "search", "gsrsearch": termo, "gsrlimit": 1,
        "gsrnamespace": 0, "prop": "extracts|info", "inprop": "url",
        "exintro": 1, "explaintext": 1, "exchars": 1000
    }
    requisicao = Request(
        f"{URL_API}?{urlencode(parametros)}",
        headers={"User-Agent": "SLID-Academico/1.0 (projetoslid@gmail.com)"}
    )
    try:
        with urlopen(requisicao, timeout=10) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))
        if "error" in dados:
            print("A API nao conseguiu realizar a pesquisa. Tente novamente depois.")
            return None
        paginas = dados.get("query", {}).get("pages", [])
        if not paginas:
            print("Nenhum resultado encontrado. Tente outro termo.")
            return None
        pagina = paginas[0]
        pesquisa = {
            "titulo": pagina["title"],
            "resumo": pagina["extract"],
            "url": pagina["fullurl"]
        }
        if not all(isinstance(valor, str) and valor.strip() for valor in pesquisa.values()):
            print("O resultado nao tem resumo disponivel. Tente outro termo.")
            return None
        return pesquisa
    except HTTPError as erro:
        print(f"A API retornou o erro HTTP {erro.code}. Tente novamente depois.")
    except (URLError, OSError):
        print("Nao foi possivel acessar a Wikipedia. Verifique sua conexao com a internet.")
    except (ValueError, KeyError, TypeError, AttributeError, IndexError):
        print("A API retornou uma resposta invalida. Tente novamente depois.")
    return None


def pesquisar_apoio(materias, historico):
    print("\n=== PESQUISAR ASSUNTO NA WIKIPEDIA ===")
    print("Busque um resumo para ajudar a estudar um assunto da aula.")
    print("A consulta usa a Wikipedia pela internet e pode ser salva na sua galeria.")
    print("\nPASSO 1 - Escolha a materia que recebera a pesquisa.")
    materia = escolher_materia(materias)
    if materia is None:
        return
    print(f"\nPASSO 2 - Informe o assunto de {materia['nome']} que deseja pesquisar.")
    print("Exemplos: derivada, linguagem Python, HTML ou banco de dados.")
    print("Digite apenas o assunto, sem precisar informar um link.")
    termo = ler_texto("Assunto (ou 0 para cancelar e voltar ao menu): ")
    if termo == "0":
        print("Pesquisa cancelada.")
        return
    print(f"\nBuscando um resumo sobre '{termo}' na Wikipedia. Aguarde...")
    pesquisa = buscar_resumo(termo)
    if pesquisa is None:
        return
    print("\nPASSO 3 - Confira se o resultado corresponde ao assunto desejado.")
    print(f"Artigo encontrado: {pesquisa['titulo']}")
    print(f"Resumo: {pesquisa['resumo']}")
    print(f"Link para ler o artigo completo: {pesquisa['url']}")
    print(f"\n1 - Guardar este resumo na galeria de {materia['nome']}")
    print("0 - Voltar ao menu sem guardar o resumo")
    confirmar = ler_inteiro("Escolha uma opcao: ", 0, 1)
    if confirmar == 1:
        materia["pesquisas"].append(pesquisa)
        historico.append(f"Pesquisa adicionada em {materia['nome']}: {pesquisa['titulo']}")
        print(f"Pesquisa adicionada a galeria de {materia['nome']}.")
        print("Para consultar depois, escolha 3 - Galeria organizada no menu principal.")
    else:
        print("O resumo nao foi guardado. Para buscar outro assunto, use a opcao 7.")


def adicionar_materia(materias, historico):
    # Adiciona uma nova materia na lista, evitando nomes vazios ou repetidos.
    print("\n=== ADICIONAR MATERIA ===")
    nome = input("Digite o nome da nova materia: ").strip()

    if nome == "":
        print("O nome da materia nao pode ficar vazio.")
        return

    for materia in materias:
        if materia["nome"].strip().casefold() == nome.casefold():
            print("Essa materia ja esta cadastrada.")
            return

    nova_materia = {
        "nome": nome,
        "capturas": [],
        "pesquisas": []
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

    print("A remocao tambem exclui os registros e pesquisas desta materia.")
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
    print("7 - Pesquisar assunto na Wikipedia (consulta a API)")
    print("8 - Desenvolvedores e contato")
    print("9 - Sair")


def menu():
    # Funcao principal que controla o fluxo do programa.
    dados = carregar_dados()
    if dados is None:
        return
    materias = dados["materias"]
    historico = dados["historico"]

    # O finally tenta salvar tambem em uma interrupcao por Ctrl+C ou fim da entrada.
    try:
        # O strip remove espacos extras digitados antes ou depois do nome.
        nome_usuario = input("Digite seu nome para interagir com o menu: ").strip()
        if nome_usuario == "":
            nome_usuario = "Visitante"
        print(f"Seja bem-vindo(a) ao menu do modo SLID, {nome_usuario}!")

        while True:
            mostrar_menu(nome_usuario)
            opcao = ler_inteiro("Escolha uma opcao entre 1 e 9: ", 1, 9)

            if opcao == 1:
                mostrar_funcionalidades()
            elif opcao == 2:
                entrar_no_modo_slid(materias, historico)
            elif opcao == 3:
                exibir_galeria(materias)
            elif opcao == 4:
                adicionar_materia(materias, historico)
            elif opcao == 5:
                remover_materia(materias, historico)
            elif opcao == 6:
                mostrar_historico(historico)
            elif opcao == 7:
                pesquisar_apoio(materias, historico)
            elif opcao == 8:
                mostrar_desenvolvedores()
            elif opcao == 9:
                break

            if opcao in (2, 4, 5, 7):
                if salvar_dados(materias, historico):
                    print("Dados salvos em dados_slid.json.")
            pausar()
    except (KeyboardInterrupt, EOFError):
        print("\nExecucao interrompida.")
    finally:
        if salvar_dados(materias, historico):
            print("\nDados salvos em dados_slid.json.")
        else:
            print("ATENCAO: as ultimas alteracoes nao foram gravadas no arquivo.")
        print("Programa encerrado.")


if __name__ == "__main__":
    menu()
