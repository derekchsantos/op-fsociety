import collections
import time

# Banco de dados em memória para rastreamento de conexões operacionais
historico_acessos = collections.defaultdict(list)
LIMITE_TENTATIVAS = 5
JANELA_TEMPO = 10  # segundos

def analisar_requisicao(ip, rota):
    agora = time.time()
    
    if "admin" in rota or "rpc/private" in rota:
        # Remove timestamps antigos fora da nossa janela de tempo operacional
        historico_acessos[ip] = [t for t in historico_acessos[ip] if agora - t < JANELA_TEMPO]
        historico_acessos[ip].append(agora)
        
        tentativas_atuais = len(historico_acessos[ip])
        print(f"[*] Requisição sensível vinda de {ip} para '{rota}'. Tentativas na janela: {tentativas_atuais}/{LIMITE_TENTATIVAS}")
        
        if tentativas_atuais >= LIMITE_TENTATIVAS:
            print(f"\033[91m[BRUTE FORCE DETECTADO] O IP {ip} ultrapassou os limites de segurança!\033[0m")
            print(f"Ação Operacional Recomendada: Bloquear IP {ip} via UFW imediatamente.")
            return False
    return True

# Simulação de ataque em tempo real
ip_atacante = "192.168.1.45"
print("[+] Simulando tentativas rápidas de força bruta...")
for i in range(6):
    analisar_requisicao(ip_atacante, "/rpc/private/login")
    time.sleep(0.5)
