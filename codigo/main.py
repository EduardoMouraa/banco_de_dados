import sys
from utils import (
    APP_DIR,
    School,
    check_extension,
    read_file,
    default_file_path
)

print("Escolha uma das opções a baixo:\n")
print("1. Importação de dados. (Caminho padrão é do arquivo é 'dados_importacao.csv')")
print("2. Relação de tipos de servidores por campi.")
print("3. Relação de docentes por disciplina de ingresso.")
print("4. Relação de disciplina de ingresso por campi e sua quantidade.\n")

try:
    option = str(input("Escolha uma das opções: "))
except:
    print("Opção não é válida.")

school = School()

if option == "1":
    file_path = str(input("Digite o caminho do arquivo (Para utilizar o caminho padrão pressione enter): "))
    if not file_path:
        file_path = default_file_path
    elif file_path[0] != "/":
        file_path = f"{APP_DIR}/{file_path}"
    
    check_extension(file_path)
    
    lido, cabecalho, dados = read_file(
        file_path=file_path
    )

    if not lido:
        print("Falha na leitura do arquivo.")
        sys.exit()
    
    school.data_import(dados=dados)
elif option == "2":
    school.get_public_servants_amount()
elif option == "3":
    school.get_professors_by_entrance_subjects()
elif option == "4":
    school.get_entrance_subjects_by_campuses()
else:
    print("Opção escolhida não é válida.")
