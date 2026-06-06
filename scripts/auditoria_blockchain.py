import hashlib
import json
import time
import smtplib
from email.mime.text import MIMEText

def calcular_hash(bloco):
    bloco_string = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(bloco_string).hexdigest()

def enviar_email_alerta(bloco_id):
    remetente = "sentinela@fsociety.com"
    destinatario = "admin@blockchain.com"
    msg = MIMEText(f"EMERGÊNCIA: Quebra de integridade detectada no Bloco #{bloco_id}.")
    msg['Subject'] = f"ALERT: Fraude na Blockchain - Bloco #{bloco_id}"
    msg['From'] = remetente
    msg['To'] = destinatario
    try:
        with smtplib.SMTP('localhost', 25) as server:
            server.sendmail(remetente, [destinatario], msg.as_string())
        print("E-mail de contingência enviado com sucesso!")
    except Exception:
        print("Erro Operacional: Servidor SMTP local offline. Log registrado.")

def auditar_blockchain(chain):
    print("\n[+] Iniciando Auditoria Criptográfica na Blockchain...")
    for idx in range(1, len(chain)):
        bloco_atual = chain[idx]
        bloco_anterior = chain[idx - 1]
        hash_calculado = calcular_hash(bloco_anterior)
        
        if bloco_atual["hash_anterior"] != hash_calculado:
            print(f"\n\033[91m[INCIDENTE] Quebra de integridade no Bloco #{bloco_atual['indice']}!\033[0m")
            enviar_email_alerta(bloco_atual["indice"])
            try:
                with open("/var/log/nginx/access.log", "a") as log_file:
                    log_file.write(f"127.0.0.1 - - [{time.strftime('%d/%b/%Y:%H:%M:%S %z')}] \"GET /blockchain/fraud HTTP/1.1\" 403 0\n")
            except PermissionError:
                with open("/tmp/access.log", "a") as log_file:
                    log_file.write(f"127.0.0.1 - - [{time.strftime('%d/%b/%Y:%H:%M:%S %z')}] \"GET /blockchain/fraud HTTP/1.1\" 403 0\n")
            return False
    print("\n\033[92m[SUCESSO] Todos os hashes estão íntegros!\033[0m")
    return True

# Inicialização e fluxo de teste
blockchain = [{"indice": 0, "timestamp": time.time(), "transacoes": ["Genesis"], "hash_anterior": "0"}]
blockchain.append({"indice": 1, "timestamp": time.time(), "transacoes": ["Tx1"], "hash_anterior": calcular_hash(blockchain[0])})

auditar_blockchain(blockchain)
print("\n[!] Adulterando Bloco #0 para forçar o alarme...")
blockchain[0]["transacoes"] = ["DADOS ADULTERADOS"]
auditar_blockchain(blockchain)
