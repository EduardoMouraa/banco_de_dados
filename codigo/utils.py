import os
import sys
import psycopg2
import decouple

CODE_PAGE = 'utf-8'
SEPARATOR = ';'
APP_DIR = os.path.dirname(os.path.abspath(__file__)) 
default_file_path = APP_DIR + '/dados_importacao.csv'

class School:
    cursor: object
    conexao: object
    
    def __init__(self):
        conexao = conecta_db()
        self.cursor = conexao.cursor()
        self.conexao = conexao

    def data_import(self, dados: list) -> None:
        try:
            for dado in dados:
                categoria, cargos, setor_siape,\
                disciplina_ingresso, setor_suap,\
                nome_servidor, funcao, jornada_trabalho,\
                telefones_institucionais,\
                matricula, curriculo,\
                campus, url_foto_74x100 = dado
                
                campi_id = self._check_or_create_data_in_table(
                    campo = "sigla",
                    dado = campus,
                    tabela = "campi",
                )
                categoria_id = self._check_or_create_data_in_table(
                    campo = "nome",
                    dado = categoria,
                    tabela = "categorias",
                )
                jornada_trabalho_id = self._check_or_create_data_in_table(
                    campo = "nome",
                    dado = jornada_trabalho,
                    tabela = "jornada_trabalho",
                )
                
                setor_siap_id = self._check_or_create_data_in_table(
                    campo = "nome",
                    dado = setor_siape,
                    tabela = "setores",
                    kwargs = {
                        "nome": setor_siape.split("/")[0],
                        "campi_id": campi_id,
                        "tipo": "siap"
                    }
                )
                setor_suap_id = self._check_or_create_data_in_table(
                    campo = "nome",
                    dado = setor_suap,
                    tabela = "setores",
                    kwargs = {
                        "nome": setor_suap.split("/")[0],
                        "campi_id": campi_id,
                        "tipo": "suap"
                    }
                )
                disciplina_ingresso_id = self._check_or_create_data_in_table(
                    campo = "nome",
                    dado = disciplina_ingresso,
                    tabela = "disciplinas"
                )
                self._check_or_create_data_in_table(
                    campo = "nome",
                    dado = cargos,
                    tabela = "cargos",
                    kwargs = {
                        "nome": cargos,
                        "jornada_trabalho_id": jornada_trabalho_id
                    }
                )
                self._check_or_create_data_in_table(
                    campo = "nome",
                    dado = nome_servidor,
                    tabela = "servidores",
                    kwargs = {
                        "nome": nome_servidor,
                        "matricula": matricula,
                        "url_foto_74x100": url_foto_74x100,
                        "curriculo": curriculo,
                        "telefones_institucionais": telefones_institucionais,
                        "campi_id": campi_id,
                        "funcao": funcao,
                        "disciplina_ingresso_id": disciplina_ingresso_id,
                        "categoria_id": categoria_id,
                        "setor_siap_id": setor_siap_id,
                        "setor_suap_id": setor_suap_id,
                    }
                )
 
            print("Dados importados com suceso")
        except Exception as e:
            print("Falha na importação dos dados. ")
            sys.exit()

    def get_public_servants_amount(self):
        # SELECT 
        #     campi.sigla as sigla_campi,
        #     categorias.nome as categoria,
        #     COUNT(categorias.nome) as qtd_categoria
        # FROM 
        #     servidores, categorias, campi
        # WHERE categorias.id=servidores.categoria_id and
        #     campi.id = servidores.campi_id
        # GROUP BY
        #     campi.sigla,
        #     categorias.nome
        # ORDER BY campi.sigla;
        sql = """\
        SELECT
            campi.sigla as sigla_campi,
            categorias.nome as categoria,
            COUNT(categorias.nome) as qtd_categoria
        FROM
            servidores
        INNER JOIN categorias ON categorias.id=servidores.categoria_id
        INNER JOIN campi ON campi.id=servidores.campi_id
        GROUP BY
            campi.sigla,
            categorias.nome
        ORDER BY campi.sigla;
        """.replace("\n", "")
        
        data = self._execute(sql=sql)
        print("\nRelação de categoria de servidores por campi:\n")
        print(f"Campi  categoria  quantidade")
        total = 0
        for response_line in data:
            campi = response_line[0].replace(" ", "")
            categoria = response_line[1]
            qtd = response_line[2]
            total += int(qtd)
            print(f"{campi} | {categoria} | {qtd}")
        
        print(f"\nQuantidade total: {total}")
    
    def get_professors_by_entrance_subjects(self):
        # OLD
        # sql = """\
        # SELECT 
        #     servidores.nome,
        #     disciplinas.nome as disciplina_ingresso,
        #     categorias.nome as categoria
        # from 
        #     servidores, categorias, disciplinas
        # where 
        #     categorias.id=servidores.categoria_id and
        #     categorias.nome='docente' and
        #     disciplinas.id = servidores.disciplina_ingresso_id
        # ORDER BY servidores.nome;
        # """.replace("\n", "")
        sql = """\
        SELECT 
            disciplinas.nome as disciplina_ingresso,
            servidores.nome as nome_servidor
        FROM
            servidores
        INNER JOIN categorias  ON categorias.id=servidores.categoria_id
        INNER JOIN disciplinas ON disciplinas.id=servidores.disciplina_ingresso_id
        WHERE
            categorias.nome='docente'
        ORDER BY disciplinas.nome, servidores.nome;
        """.replace("\n", "")
        
        data = self._execute(sql=sql)
        print("\nRelação de docentes por disciplina de ingresso:\n")
        print(f"Disciplina_ingresso")
        for response_line in data:
            disciplina_ingresso = response_line[0]
            nome = response_line[1]
            print(f"{disciplina_ingresso} | {nome}")
    
    def get_entrance_subjects_by_campuses(self):
        # sql = """\
        # SELECT 
        #     disciplinas.nome as disciplina_ingresso,
        #     campi.sigla,
        #     COUNT(disciplinas.nome) as qtd_disciplinas
        # from 
        #     disciplinas, campi, servidores
        # where 
        #     campi.id=servidores.campi_id and
        #     disciplinas.id = servidores.disciplina_ingresso_id
        # GROUP BY
        #     disciplinas.nome,
        #     campi.sigla
        # ORDER BY campi.sigla;
        # """
        sql = """\
        SELECT 
            disciplinas.nome as disciplina_ingresso,
            campi.sigla as campi,
            COUNT(disciplinas.nome) as qtd_disciplinas
        from 
            servidores
        INNER JOIN campi ON campi.id=servidores.campi_id
        INNER JOIN disciplinas ON disciplinas.id = servidores.disciplina_ingresso_id
        GROUP BY
            disciplinas.nome,
            campi.sigla
        ORDER BY disciplinas.nome, campi.sigla;
        """.replace("\n", "")
        
        data = self._execute(sql=sql)
        print("\nRelação de disciplina de ingresso por campi:\n")
        print(f"Disciplina_ingresso  Campi   qtd_disciplinas")
        total = 0
        for response_line in data:
            disciplina_ingresso = response_line[0]
            Campi = response_line[1]
            qtd_disciplinas = response_line[2]
            total += int(qtd_disciplinas)
            print(f"{disciplina_ingresso} | {Campi} | {qtd_disciplinas}")
        print(f"Total das disciplinas: {total}")
    
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

    def _check_data(
        self,
        campo: str,
        dado: str,
        tabela: str,
        kwargs: dict = {}
    ):
        sql = ""
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
        return dados

    def _check_or_create_data_in_table(
        self,
        campo: str,
        dado: str,
        tabela: str,
        kwargs: dict = {}
    ) -> bool:
        
        dados = self._check_data(
            campo = campo,
            dado = dado,
            tabela = tabela,
            kwargs = kwargs
        )
        
        if not dados:
            dados = self._create_data_in_table(
                tabela=tabela,
                dados=dado,
                campos=campo,
                kwargs=kwargs
            )

            dados = self._check_data(
                campo = campo,
                dado = dado,
                tabela = tabela,
                kwargs = kwargs
            )
        
        if dados:
            return dados[0][0]
        else:
            return False

    def _execute(
        self,
        sql: str,
        commit: bool = False
    ) -> str:
        try:
            self.cursor.execute(sql)
        except Exception as e:
            e = str(e)
            if "does not exist" in e:
                print("\nPara realizar consultas ou importações é necessário a criação da estrutura do banco de dados.")
                sys.exit()
            else:
                print(e)
                sys.exit()

        if commit:
            dados = self.conexao.commit()
        else:
            dados = self.cursor.fetchall()
        
        return dados


def check_extension(file_path) -> None:
    extension = file_path.split(".")[-1]
    if extension != "csv":
        print(f"\nExtensão {extension} do arquivo não suportada.")
        sys.exit()
  
def read_file(file_path: str) -> tuple:
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

def conecta_db():
    server = decouple.config("SERVER", default="", cast=str)
    database = decouple.config("DATABASE", default="", cast=str)
    user = decouple.config("USERDB", default="", cast=str)
    passwd = decouple.config("PASSWD", default="", cast=str)
    port = decouple.config("PORT", default="", cast=str)

    if not server:
        print("\nServer não encontrado.")
        sys.exit()
        
    if not database:
        print("\nNome do banco de dados não encontrado.")
        sys.exit()

    if not user:
        print("\nUser do banco de dados não encontrado.")
        sys.exit()

    if not passwd:
        print("\nSenha do banco de dados não encontrado.")
        sys.exit()
    
    conexao = None
    try:
        conexao = psycopg2.connect(f"dbname={database} user={user} host={server} password={passwd} port={port}")
    except Exception as e:
        conexao = f"\nFalha na conexão ao banco: {e}"
        print(conexao)
        sys.exit()
    
    if not conexao:
        conexao = f"\nFalha na conexão ao banco."
        sys.exit()
    
    return conexao
