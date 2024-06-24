import zipfile
import os
import re
from datetime import datetime
import pandas as pd
from Captura_FTP import capturar_e_descompactar_arquivo

def tratativa_excel(pasta_local):
    if not pasta_local or not os.path.exists(pasta_local):
        print("Pasta local não encontrada ou inválida.")
        return False

    data_atual = datetime.now().date()
    data_para_nome = data_atual.strftime("%Y%m%d")
    regex_excel = re.compile(f"RESUMIDA_BL(0[1-9]|1[0-1])_{data_para_nome}\\.xlsx")

    arquivos_excel = [f for f in os.listdir(pasta_local) if regex_excel.match(f)]
    if not arquivos_excel:
        print("Nenhum arquivo Excel correspondente encontrado.")
        return False

    data_frames = []
    for i, arquivo in enumerate(arquivos_excel):
        file_path = os.path.join(pasta_local, arquivo)
        df = pd.read_excel(file_path)
        if i == 0:
            data_frames.append(df)
        else:
            data_frames.append(df.iloc[1:])  # Exclui o cabeçalho (primeira linha) a partir do segundo arquivo

    resultado = pd.concat(data_frames, ignore_index=True)
    output_file = os.path.join(pasta_local, f"UNIFICADO_RESUMIDA_BL_{data_para_nome}.xlsx")
    resultado.to_excel(output_file, index=False)
    print(f"Arquivo unificado salvo em: {output_file}")

    return True

# Teste as funções diretamente para ver o resultado imediato
pasta_local = capturar_e_descompactar_arquivo()
if pasta_local:
    tratativa_excel(pasta_local)

 

