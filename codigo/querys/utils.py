import decouple
import psycopg2

# ------------------------------------------------------------
def conecta_db():
    server = decouple.config("SERVER", default="", cast=str)
    database = decouple.config("DATABASE", default="", cast=str)
    user = decouple.config("USERDB", default="", cast=str)
    passwd = decouple.config("PASSWD", default="", cast=str)
    port = decouple.config("PORT", default="", cast=str)

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
        print("gereads")
        conexao = psycopg2.connect(f'dbname={database} user={user} host={server} password={passwd} port={port}')
        print("gere")
    except Exception as e:
        print("ERRO: ", e)
        conexao = f'ERRO: {sys.exc_info()[0]}'
    else:
        print(conexao)
        conectado = True
    finally:
        return conectado, conexao