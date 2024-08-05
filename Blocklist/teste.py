import pandas as pd

# Lê o arquivo .txt
df = pd.read_csv(r'C:\\Santander\\PROJETO_DNR_SANTANDER\\Blocklist\\20240731\\UNIFICADO_RESUMIDA_BL_teste.txt', delimiter='\t')

# Converte para um novo arquivo .txt com separador por vírgulas
df.to_csv('UNIFICADO_RESUMIDA_BL_teste_OK.txt', sep=',', index=False)

print("Arquivo convertido com sucesso!")