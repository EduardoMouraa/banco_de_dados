import sys
from constantes import *
import psycopg2
import decouple

class Escola:
    cursor: object
    conexao: object
    
    def __init__(self, cursor: object, conexao: object):
        self.cursor = cursor
        self.conexao = conexao

    def _create_data_in_table(
        self,
        tabela: str,
        dados: str,
        campos: str,
        kwargs: dict = {},
    ):
        if not kwargs:
            sql = f"""\
            INSERT INTO {tabela} 
                ({campos}) VALUES (\'{dados}\');
            """.replace("\n", "")
        else:
            campos = ""
            values = ""
            for kwarg in kwargs:
                campos += f"{kwarg}, "
                values += f"'{kwargs[kwarg]}', "
            
            campos = campos[:-2]
            values = values[:-2]
            
            sql = f"""\
            INSERT INTO {tabela} 
                ({campos}) VALUES ({values});
            """.replace("\n", "")
        
        dados = self._execute(
            sql=sql,
            commit=True
        )
        return dados

    def check_or_create_data_in_table(
        self,
        campo: str,
        dado: str,
        tabela: str,
        kwargs: dict = {}
    ) -> bool:
        
        if not kwargs:
            sql = f"""\
            SELECT * FROM {tabela}
                WHERE {campo}=\'{dado}\';
            """.replace("\n", "")
        else:
            sql = f"""\
            SELECT * FROM {tabela}
                WHERE 
            """.replace("\n", "")
            for kwarg in kwargs:
                sql +=f"{kwarg}=\'{kwargs[kwarg]}\' AND "
            
            sql = sql[:-4]
        
        dados = self._execute(sql=sql)
        
        if not dados:
            dados = self._create_data_in_table(
                tabela=tabela,
                dados=dado,
                campos=campo,
                kwargs=kwargs
            )
        
        if dados:
            return dados[0][0]
        else:
            return False

    def _execute(
        self,
        sql: str,
        commit: bool = False,
    ) -> str:
        self.cursor.execute(sql)
        
        if commit:
            dados = self.conexao.commit()
        else:
            dados = self.cursor.fetchall()
        
        return dados

def importar_dados(
    cabecalho: list,
    dados: list
):
    conectado, conexao = conecta_db()

    if not conectado:
        print(conexao)
        sys.exit()
    
    cursor = conexao.cursor()
    escola = Escola(
        cursor = cursor,
        conexao = conexao
    )
    for dado in dados:
        categoria, cargos, setor_siape,\
        disciplina_ingresso, setor_suap,\
        nome, funcao, jornada_trabalho,\
        telefones_instituicionais,\
        matricula, curriculo_lates,\
        campus, url_foto_75x100 = dado
        
        campi_id = escola.check_or_create_data_in_table(
            campo = "sigla",
            dado = campus,
            tabela = "campi",
        )
        escola.check_or_create_data_in_table(
            campo = "nome",
            dado = categoria,
            tabela = "categorias",
        )
        escola.check_or_create_data_in_table(
            campo = "name",
            dado = jornada_trabalho,
            tabela = "jornada_trabalho",
        )
        escola.check_or_create_data_in_table(
            campo = "name",
            dado = jornada_trabalho,
            tabela = "jornada_trabalho"
        )
        escola.check_or_create_data_in_table(
            campo = "nome",
            dado = setor_siape,
            tabela = "setores",
            kwargs = {
                "nome": setor_siape.split("/")[0],
                # "campi_id": campi_id,
                "campus": campi_id,
                "type": "siap"
            }
        )
        
        print(dado)

# ------------------------------------------------------------
def ler_arquivo(file_path: str) -> tuple:
    lido = False
    cabecalho = []
    dados_retorno = []
    try:
        arq_ = open(file_path, 'r', encoding=CODE_PAGE)
    except FileNotFoundError:
        dados_retorno = f'\nERRO: Arquivo Inexistente...'
    except:
        dados_retorno = f'\nERRO: {sys.exc_info()[0]}'
    else:
        count = 0
        while True:
            linha = arq_.readline()[:-1]
            if not linha: break
            lista_linha = linha.split(SEPARATOR)
            if count == 0:
                cabecalho.append(lista_linha)
            else:
                dados_retorno.append(lista_linha)
            count +=1
            lido = True
            
        arq_.close()
    finally:
        return lido, cabecalho, dados_retorno

# ------------------------------------------------------------
def conecta_db():
    server = decouple.config("SERVER", default="", cast=str)
    database = decouple.config("DATABASE", default="", cast=str)
    user = decouple.config("USERDB", default="", cast=str)
    passwd = decouple.config("PASSWD", default="", cast=str)

    if not server:
        print("Server não encontrado.")
        sys.exit()
        
    if not database:
        print("Nome do banco de dados não encontrado.")
        sys.exit()

    if not user:
        print("User do banco de dados não encontrado.")
        sys.exit()

    if not passwd:
        print("Senha do banco de dados não encontrado.")
        sys.exit()
    
    conectado = False
    conexao   = None
    try:
        conexao = psycopg2.connect(f'dbname={database} user={user} host={server} password={passwd}')
    except:
        conexao = f'ERRO: {sys.exc_info()[0]}'
    else:
        conectado = True
    finally:
        return conectado, conexao