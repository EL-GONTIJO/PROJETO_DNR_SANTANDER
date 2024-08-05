import paramiko
import base64
from datetime import datetime
import os
import zipfile
import re
import pandas as pd

def capturar_e_descompactar_arquivo():
    host = "186.231.6.25"
    port = 22
    username = "sftp.santanderApoio_001"
    password = base64.b64decode("Y3dHUHJqYVB3dXY5").decode("utf-8")

    data_atual = datetime.now().date()
    data_para_nome = data_atual.strftime("%Y%m%d")

    regex_arquivo = f"BLOQUEADOS_COBRANCA_{data_para_nome}_.*\\.zip"

    pasta_local = f"./{data_para_nome}"
    os.makedirs(pasta_local, exist_ok=True)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=host, port=port, username=username, password=password)
        print("Conexão SFTP estabelecida.")

        sftp_client = ssh_client.open_sftp()
        caminho_diretorio = "/upload/bl/base"
        sftp_client.chdir(caminho_diretorio)
        print(f"Acessando diretório: {caminho_diretorio}")

        file_list = sftp_client.listdir(".")
        print(f"Arquivos encontrados em {caminho_diretorio}:")

        arquivo_encontrado = None
        for file in file_list:
            print(file)
            if re.match(regex_arquivo, file):
                arquivo_encontrado = file
                break

        if arquivo_encontrado:
            local_path = os.path.join(pasta_local, arquivo_encontrado)
            sftp_client.get(arquivo_encontrado, local_path)
            print(f"Arquivo {arquivo_encontrado} baixado como {arquivo_encontrado} em {pasta_local}")

            with zipfile.ZipFile(local_path, "r") as zip_ref:
                zip_ref.extractall(pasta_local)
            print(f"Arquivo {arquivo_encontrado} descompactado em {pasta_local}")
            return pasta_local
        else:
            print(f"Arquivo correspondente à nomenclatura {regex_arquivo} não encontrado em {caminho_diretorio}")
            return None

    except Exception as e:
        print(f"Erro ao conectar ou operar no SFTP: {e}")
        return None
    finally:
        if "sftp_client" in locals():
            sftp_client.close()
        ssh_client.close()
        print("Conexão SFTP fechada.")

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

pasta_local = capturar_e_descompactar_arquivo()
if pasta_local:
    tratativa_excel(pasta_local)

