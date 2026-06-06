import time

# Whitelist de IPs e Datacenters autorizados para gerenciar o nó Blockchain
IPS_PERMITIDOS = ["127.0.0.1", "10.0.0.5", "192.168.1.100"]

print("Inicializando Módulo de Auditoria Geográfica e Antimetadados...")

def verificar_anomalia_acesso(ip, usuario):
    print(f"\n[*] Analisando metadados de acesso de [{usuario}] vindo do IP: {ip}")
    
    if ip not in IPS_PERMITIDOS:
        print(f"\033[41m\033[37m[ALERTA GEOGRÁFICO]\033[0m Acesso Suspeito detectado!")
        print(f"O usuário '{usuario}' tentou disparar comandos de infraestrutura fora da Whitelist corporativa.")
        print("Ação Operacional: Notificação emergencial encaminhada e IP isolado de forma preventiva.")
        return False
        
    print("\033[92m Origem Autorizada: IP correspondente ao perímetro seguro do Datacenter.\033[0m")
    return True

# Simulação 1: Acesso interno legítimo do mrrobot
verificar_anomalia_acesso("127.0.0.1", "mrrobot")

# Simulação 2: Tentativa de login vinda de um IP externo malicioso da internet pública
verificar_anomalia_acesso("203.0.113.50", "hacker_darkarmy")
