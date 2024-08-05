import zipfile
import os
import re
from datetime import datetime
import pandas as pd
#from Captura_FTP import capturar_e_descompactar_arquivo

def tratativa_excel(pasta_local):
    if not pasta_local or not os.path.exists(pasta_local):
        print("Pasta local não encontrada ou inválida.")
        return False

    data_atual = datetime.now().date()
    data_para_nome = data_atual.strftime("%Y%m%d")
    regex_excel = re.compile(f"RESUMIDA_BL([1-9]|1[0-9])_{data_para_nome}\\.xlsx")

    arquivos_excel = [f for f in os.listdir(pasta_local) if regex_excel.match(f)]
    if not arquivos_excel:
        print("Nenhum arquivo Excel correspondente encontrado.")
        return False

    # Adiciona a linha para imprimir os arquivos Excel identificados
    print(f"Arquivos Excel identificados para unificação: {arquivos_excel}")

    data_frames = []
    for i, arquivo in enumerate(arquivos_excel):
        file_path = os.path.join(pasta_local, arquivo)
        df = pd.read_excel(file_path, dtype={'cpf_cnpj': str, 'telefone': str})
        # Conta e imprime o número de linhas do DataFrame atual
        print(f"{arquivo}: {len(df)} linhas")
        if i == 0:
            data_frames.append(df)
        else:
            data_frames.append(df.iloc[1:])  # Exclui o cabeçalho (primeira linha) a partir do segundo arquivo

    resultado = pd.concat(data_frames, ignore_index=True)
    
    # Adiciona a linha para imprimir o número de linhas do DataFrame resultante
    print(f"Número de linhas do DataFrame unificado: {len(resultado)}")

    # Salva o DataFrame resultante em um arquivo .txt
    output_file = os.path.join(pasta_local, f"UNIFICADO_RESUMIDA_BL_{data_para_nome}.txt")
    resultado.to_csv(output_file, sep=',', index=False)
    print(f"Arquivo unificado salvo em: {output_file}")

    return True
 


pasta_local = (r"C:\\Santander\\PROJETO_DNR_SANTANDER\\Blocklist\\20240731")
if pasta_local:
    tratativa_excel(pasta_local)

 

  