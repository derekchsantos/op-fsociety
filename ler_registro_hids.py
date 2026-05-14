import os
import json
from cryptography.fernet import Fernet

CHAVE_MESTRA = "hids.key"
BASE_DADOS_CIFRADA = "registro_seguro.enc"

print("[+] Iniciando utilitário de decodificação forense...")

# 1. Carrega a chave mestra de segurança
if not os.path.exists(CHAVE_MESTRA) or not os.path.exists(BASE_DADOS_CIFRADA):
    print("\033[91m[ERRO] Chave mestra ou base de dados cifrada ausente no diretório!\033[0m")
    exit(1)

with open(CHAVE_MESTRA, "rb") as f:
    chave = f.read()

cipher = Fernet(chave)

# 2. Lê e descriptografa os dados estruturados do HIDS
with open(BASE_DADOS_CIFRADA, "rb") as f:
    dados_criptografados = f.read()

try:
    dados_decifrados = cipher.decrypt(dados_criptografados).decode()
    base_hashes = json.loads(dados_decifrados)
    
    print("\n\033[92m[SUCESSO] Base de dados decifrada perfeitamente via AES-128:\033[0m")
    print(json.dumps(base_hashes, indent=4))
except Exception as e:
    print(f"\033[41m[ERRO CRÍTICO] Falha ao descriptografar. Chave inválida ou dados corrompidos: {e}\033[0m")
