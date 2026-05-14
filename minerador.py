import hashlib
import time

def minerar_bloco(indice, transacoes, hash_anterior, dificuldade):
    print(f"\n[🔨] Iniciando mineração do Bloco #{indice}...")
    alvo = "0" * dificuldade
    nonce = 0
    inicio = time.time()
    
    while True:
        conteudo = f"{indice}{transacoes}{hash_anterior}{nonce}".encode()
        hash_resultado = hashlib.sha256(conteudo).hexdigest()
        
        if hash_resultado.startswith(alvo):
            tempo_gasto = time.time() - inicio
            print(f"\033[92m[✓] Bloco #{indice} Minerado com Sucesso em {tempo_gasto:.2f}s!\033[0m")
            print(f"[*] Nonce Encontrado: {nonce}")
            print(f"[*] Hash Válido: {hash_resultado}")
            return hash_resultado, nonce
        nonce += 1

# Teste operacional com dificuldade de 4 zeros (Aumente para 5 ou 6 se quiser exigir mais CPU)
dificuldade_da_rede = 4
hash_genesis = "0000000000000000000000000000"
minerar_bloco(1, ["Tx: Alice -> Bob (1.5 ETH)"], hash_genesis, dificuldade_da_rede)
