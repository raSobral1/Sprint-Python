# SLID - Menu em Python

Versao academica do projeto See, Listen and Identify. Os registros de quadro,
fala e resumo sao digitados manualmente; esta versao nao captura imagens nem audio.

## Como executar

Com Python 3 instalado, abra o terminal na pasta do projeto e execute:

```sh
python menuJovi.py
```

Nao e necessario instalar bibliotecas. Apenas a pesquisa na Wikipedia precisa
de internet; as demais funcionalidades sao locais.

## O que foi acrescentado

- **Persistencia:** `carregar_dados()` recupera materias, capturas, pesquisas e
  historico de `dados_slid.json`. `salvar_dados()` grava depois das operacoes
  de cadastro, remocao, registro e pesquisa, e tambem ao sair.
- **API externa:** a opcao **7** pesquisa um assunto na Wikipedia em portugues,
  mostra titulo, resumo e fonte, e permite guardar o resultado em uma materia.
  `buscar_resumo()` faz a requisicao com `urllib.request`, com limite de espera
  de 10 segundos. `pesquisar_apoio()` cuida da interacao com o usuario.
- **Validacoes:** `ler_texto()` impede registros vazios. `validar_dados()`
  verifica a estrutura do arquivo. Foram mantidas as validacoes de numeros,
  nomes de materias e confirmacao da remocao.
- **Tratamento de erros:** mensagens para falhas de leitura/escrita, JSON
  invalido, falta de conexao, erro HTTP e resposta invalida da API. Um arquivo
  invalido nao e substituido automaticamente.
- **Organizacao:** funcoes com parametros e retornos, uma unica pausa ao final
  de cada funcionalidade e `if __name__ == "__main__"` para iniciar o menu
  somente ao executar o arquivo diretamente. A opcao **8** mostra desenvolvedores
  e contato; a opcao **9** encerra o programa.

## Integracao por arquivo

O arquivo `dados_slid.json` e criado automaticamente ao usar o programa e fica
na mesma pasta de `menuJovi.py`. Pode ser lido por outra parte do projeto,
como uma interface web. Sua estrutura e:

```json
{
    "materias": [
        {
            "nome": "Python",
            "capturas": [
                {"quadro": "Funcoes", "fala": "Usar parametros", "resumo": "Reutilizar codigo"}
            ],
            "pesquisas": [
                {"titulo": "Titulo do artigo", "resumo": "Resumo recebido da API", "url": "https://pt.wikipedia.org/..."}
            ]
        }
    ],
    "historico": ["Captura adicionada na materia Python"]
}
```

Cada materia deve ter `nome`, `capturas` e `pesquisas`, mesmo que as listas
estejam vazias. Para integrar, a outra parte deve ler esse formato; se for
editar o arquivo, feche o menu antes para evitar sobrescrever alteracoes.
O repositorio atual contem somente o programa de terminal: a leitura pela
outra parte da solucao devera ser implementada nessa outra parte.

## Roteiro para demonstrar

1. Cadastre uma materia pela opcao 4.
2. Use a opcao 2 para registrar quadro, fala e resumo.
3. Use a opcao 7 e siga os passos: escolha a materia, digite um assunto como
   `derivada`, confira o artigo encontrado e digite 1 para guardar o resumo.
   Nao precisa informar um link. Digite 0 no campo de assunto para cancelar
   ou na confirmacao para voltar sem guardar o resultado.
4. Consulte os registros e a pesquisa na galeria, opcao 3.
5. Veja as acoes no historico, opcao 6.
6. Saia com 9 e abra novamente para mostrar que os dados continuam salvos.
7. Mostre o JSON para explicar a persistencia e a integracao por arquivo.

Documentacao da API utilizada:
[busca](https://www.mediawiki.org/wiki/API:Search) e
[resumos em texto](https://www.mediawiki.org/wiki/Extension:TextExtracts#API).

## Verificacao realizada

O programa foi verificado com Python 3.13.7 portatil, sem instalar dependencias.
Foram testados o fluxo do menu, entradas invalidas, cadastro, duplicidade,
remocao, galeria, historico, persistencia entre execucoes e interrupcao por Ctrl+C.
Os casos de falha da API e dos arquivos foram simulados em testes isolados.
Tambem foi realizada uma consulta real a API com o termo `derivada`, que retornou
o artigo **Derivada**, seu resumo e o endereco da fonte.

## Integrantes

Erick Ripari Gomes - 569441

Fabricio Denig de Avila - 570980  

Guilherme Mazzini Nunes Canno - 573183

Luan Schinello Garbin - 571276

Rafael Taboada Sobral - 569527
