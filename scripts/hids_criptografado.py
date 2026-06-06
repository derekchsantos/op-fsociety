import os
import json
import hashlib
from cryptography.fernet import Fernet

BASE_DADOS_CIFRADA = "registro_seguro.enc"
CHAVE_MESTRA = "hids.key"
ARQUIVOS_CRITICOS = ["sentinela.sh", "auditoria_blockchain.py"]

def gerar_hash_arquivo(caminho):
    if not os.path.exists(caminho): return None
    hasher = hashlib.sha256()
    with open(caminho, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

# 1. Gerenciamento de Chaves Operacionais
if not os.path.exists(CHAVE_MESTRA):
    chave = Fernet.generate_key()
    with open(CHAVE_MESTRA, "wb") as f: f.write(chave)
else:
    with open(CHAVE_MESTRA, "rb") as f: chave = f.read()

cipher = Fernet(chave)

# 2. Inicialização ou Auditoria da Base de Hashes
if not os.path.exists(BASE_DADOS_CIFRADA):
    registro_puro = {arq: gerar_hash_arquivo(arq) for arq in ARQUIVOS_CRITICOS}
    dados_criptografados = cipher.encrypt(json.dumps(registro_puro).encode())
    with open(BASE_DADOS_CIFRADA, "wb") as f: f.write(dados_criptografados)
    print("\033[94m[HIDS SIMÉTRICO] Registro inicial gerado e criptografado com AES/Fernet.\033[0m")
else:
    with open(BASE_DADOS_CIFRADA, "rb") as f: dados_cifrados_disco = f.read()
    registro_decifrado = json.loads(cipher.decrypt(dados_cifrados_disco).decode())
    print("[+] Executando varredura HIDS Criptografada...")
    
    for arq in ARQUIVOS_CRITICOS:
        hash_atual = gerar_hash_arquivo(arq)
        if hash_atual != registro_decifrado.get(arq):
            print(f"\033[41m\033[37m[ INSTABILIDADE HIDS]\033[0m Violação! O arquivo '{arq}' foi adulterado!")
