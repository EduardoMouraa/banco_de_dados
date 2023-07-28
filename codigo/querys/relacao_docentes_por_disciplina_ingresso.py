
from utils import conecta_db
import sys

conectado, conexao = conecta_db()

if not conectado:
	print(conexao)
	sys.exit()

sql = """\
SELECT 
	servidores.nome,
	disciplinas.nome as disciplina_ingresso,
	categorias.nome as categoria
from 
	servidores, categorias, disciplinas
where 
	categorias.id=servidores.categoria_id and
	categorias.nome='docente' and
	disciplinas.id = servidores.disciplina_ingresso_id
ORDER BY servidores.nome;
"""

cursor = conexao.cursor()
cursor.execute(sql)

dados = cursor.fetchall()

print("Relação de docentes por disciplina de ingresso:\n")
for dado in dados:
    nome = dado[0]
    disciplina_ingresso = dado[1]
    categoria = dado[2]
    print(f"{nome} | {disciplina_ingresso} | {categoria}")


