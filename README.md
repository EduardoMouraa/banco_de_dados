# Repositório para disciplina de banco_de_dados do curso de redes de computadores

### Primeiros passos

#### Criação de ambiente virtual
```bash
$ python -m venv .venv
```
Para acessar o ambiente virtual execute:

Linux:
```bash
$ source .venv/bin/activate
```

Windows:
```bash
$ .venv/Scripts/Activate
```

Agora crie um arquivo chamado **.env** e adicione os seguintes valores ao arquivo substituindo o que estiver entre **<>**:
```
SERVER=<IP_DO_SERVIDOR_DO_BANCO>
DATABASE=<NOME_DO_BANCO_DE_DADOS>
USERDB=<USUARIO_DO_BANCO_DE_DADOS>
PASSWD=<SENHA_DO_BANCO_DE_DADOS>
```

## Acessando a pasta de códigos:
```bash
$ cd codigo/importacao
```

## Para rodar a importação de dados execute:
```bash
$ python importar_dados.py
```
