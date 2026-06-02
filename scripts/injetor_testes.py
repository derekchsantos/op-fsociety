# @author Derek Christopher
# -*- coding: utf-8 -*-

import requests
import time
import os

API_NGINX = "http://127.0.0.1:1337"

print("[+] Inicializando Injetor de Testes Automatizado...")

def testar_cenario_1():
    print("\n Simulando Cenário 1: Erro de Gateway (Simulação via log)...")
    try:
        # Escreve um log simulado de erro 502 diretamente para ativar a Sentinela
        with open("/tmp/access.log", "a") as f:
            f.write('127.0.0.1 - - [' + time.strftime('%d/%b/%Y:%H:%M:%S %z') + '] "GET /api/v1/rpc HTTP/1.1" 502 0\n')
        print("Evento de Blockchain Offline injetado no log.")
    except Exception as e:
        print(f"Falha ao injetar no log: {e}")

def testar_cenario_2():
    print("\n Simulando Cenário 2: Varredura de Rota Sensível (/wallet)...")
    # Dispara contra o Nginx real na porta 1337
    try:
        response = requests.get(f"{API_NGINX}/wallet", timeout=2)
        print(f"Requisição enviada. Resposta HTTP do Nginx: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao Nginx na porta 1337.")

def testar_cenario_3():
    print("\n Simulando Cenário 3: Ataque de Fraude detectado pela Blockchain...")
    try:
        # Injeta a linha de fraude diretamente na ponte de logs que o Shell lê
        with open("/tmp/access.log", "a") as f:
            f.write('127.0.0.1 - - [' + time.strftime('%d/%b/%Y:%H:%M:%S %z') + '] "GET /blockchain/fraud HTTP/1.1" 403 0\n')
        print("Alerta máximo de integridade violada injetado.")
    except Exception as e:
        print(f"Falha ao injetar no log: {e}")

# Execução em lote de todas as validações operacionais
testar_cenario_1()
time.sleep(2)
testar_cenario_2()
time.sleep(2)
testar_cenario_3()

print("\n Injeção concluída. Verifique os alertas na tela do seu 'sentinela.sh'!")
