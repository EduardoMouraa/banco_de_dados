
from utils import conecta_db
import sys

conectado, conexao = conecta_db()

if not conectado:
	print(conexao)
	sys.exit()

sql = """\
SELECT 
	campi.sigla,
	categorias.nome,
	COUNT(categorias.nome) as qtd_categoria
FROM 
	servidores, categorias, campi
WHERE categorias.id=servidores.categoria_id and
	campi.id = servidores.campi_id
GROUP BY
	campi.sigla,
	categorias.nome
ORDER BY campi.sigla;
"""

cursor = conexao.cursor()
cursor.execute(sql)

dados = cursor.fetchall()

print("Relação de categoria de servidores por campi:\n")
print(f"Campi  categoria  quantidade")
for dado in dados:
	campi = dado[0].replace(" ", "")
	categoria = dado[1]
	qtd = dado[2]
	print(f"{campi} | {categoria} | {qtd}")
