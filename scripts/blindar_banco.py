# @author Derek Christopher
# -*- coding: utf-8 -*-

import os
from cryptography.fernet import Fernet

DB_FILE = "siem_alertas.db"
KEY_FILE = "db_master.key"

print("Iniciando Sistema de Blindagem de Dados em Disco...")

# Inicializa ou lê a chave criptográfica master
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as kf: kf.write(key)
else:
    with open(KEY_FILE, "rb") as kf: key = kf.read()

cipher = Fernet(key)

def cifrar_banco():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f: dados_puros = f.read()
        dados_cifrados = cipher.encrypt(dados_puros)
        with open(DB_FILE, "wb") as f: f.write(dados_cifrados)
        print("Sucesso: Banco de dados SQLite totalmente criptografado em disco.")
    else:
        print("Erro: Arquivo de banco de dados não encontrado para cifragem.")

def decifrar_banco():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f: dados_cifrados = f.read()
        try:
            dados_puros = cipher.decrypt(dados_cifrados)
            with open(DB_FILE, "wb") as f: f.write(dados_puros)
            print("[✓] Sucesso: Banco de dados SQLite descriptografado e pronto para o Flask.")
        except Exception:
            print("[*] O arquivo já parece estar descriptografado ou em formato texto puro.")

# Mapeia os argumentos de linha de comando para automação
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "cifrar": cifrar_banco()
    elif sys.argv[1] == "decifrar": decifrar_banco()
