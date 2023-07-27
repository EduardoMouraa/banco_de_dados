# banco_de_dados



# Primeiros passos

## Criação de ambiente virtual
`
$ python -m venv .venv
`
Para acessar o ambiente virtual execute:

Linux:
`
$ source .venv/bin/activate
`
Windows:
$ .venv/Scripts/Activate

Agora crie um arquivo chamado **.env** e adicione os seguintes valores ao arquivo substituindo o que estiver entre **<>**:
`
SERVER=<IP_DO_SERVIDOR_DO_BANCO>
DATABASE=<NOME_DO_BANCO_DE_DADOS>
USERDB=<USUARIO_DO_BANCO_DE_DADOS>
PASSWD=<SENHA_DO_BANCO_DE_DADOS>
`
## Acessando a pasta de códigos:
`
$ cd codigo/importacao
`

## Para rodar a importação de dados execute:
`
$ python importar_dados.py
`