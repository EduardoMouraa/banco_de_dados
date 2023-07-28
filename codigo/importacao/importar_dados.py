import os
import sys
from utils import ler_arquivo, importar_dados

APP_DIR = os.path.dirname(os.path.abspath(__file__)) 

# ------------------------------------------------------------
# Lendo arquivo de input
lido, cabecalho, dados = ler_arquivo(
    file_path=APP_DIR + '/dados_importacao.csv'
)

if not lido:
    print("Falha na leitura do arquivo.")
    sys.exit()

print(f"Importando dados...")
importar_dados(
    cabecalho = cabecalho,
    dados = dados
)

print(f"Dados importados com sucesso.")
