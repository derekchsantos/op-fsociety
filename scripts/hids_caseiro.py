import hashlib
import os
import json

BASE_DADOS_HASHES = "registro_seguro.json"
ARQUIVOS_CRITICOS = ["sentinela.sh", "auditoria_blockchain.py"]

def gerar_hash_arquivo(caminho):
    if not os.path.exists(caminho): return None
    hasher = hashlib.sha256()
    with open(caminho, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

# Inicializa ou audita a base de assinaturas
if not os.path.exists(BASE_DADOS_HASHES):
    registro = {arq: gerar_hash_arquivo(arq) for arq in ARQUIVOS_CRITICOS}
    with open(BASE_DADOS_HASHES, "w") as f: json.dump(registro, f)
    print("\033[94m[SISTEMA] Registro inicial de integridade criado com sucesso.\033[0m")
else:
    with open(BASE_DADOS_HASHES, "r") as f: registro_antigo = json.load(f)
    print("[+] Executando varredura HIDS nos arquivos críticos...")
    
    for arq in ARQUIVOS_CRITICOS:
        hash_atual = gerar_hash_arquivo(arq)
        if hash_atual != registro_antigo.get(arq):
            print(f"\033[41m\033[37m[🚨 HIDS INCIDENTE]\033[0m O arquivo '{arq}' foi MODIFICADO ou adulterado!")
