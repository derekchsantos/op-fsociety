import base64
from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError

print("[+] Iniciando Módulo de Assinatura Digital ECDSA (Padrão SECP256k1)...")

# 1. Geração do par de chaves (Privada e Pública)
chave_privada = SigningKey.generate(curve=SECP256k1)
chave_publica = chave_privada.verifying_key

# Exportando as chaves em formato legível (String/Bytes)
chave_privada_string = base64.b64encode(chave_privada.to_string()).decode()
chave_publica_string = base64.b64encode(chave_publica.to_string()).decode()

print(f"[*] Chave Privada (Manter em Segredo): {chave_privada_string[:20]}...")
print(f"[*] Chave Pública (Endereço da Carteira): {chave_publica_string[:20]}...")

# 2. Criando os dados operacionais da transação
dados_transacao = "Origem: Carteira_A | Destino: Carteira_B | Valor: 10.5 BTC"
print(f"\n[+] Assinando transação: '{dados_transacao}'")

# 3. Assinando digitalmente a transação com a Chave Privada
assinatura = chave_privada.sign(dados_transacao.encode('utf-8'))
assinatura_legivel = base64.b64encode(assinatura).decode()
print(f"Assinatura Digital Gerada: {assinatura_legivel[:30]}...")

# 4. FUNÇÃO OPERACIONAL DE VALIDAÇÃO (Auditoria de Rede)
def verificar_autenticidade(dados, assin, ch_pub):
    try:
        # Tenta validar a assinatura usando a chave pública correspondente
        ch_pub.verify(assin, dados.encode('utf-8'))
        print("\n\033[92m[SUCESSO] Transação Válida! Assinatura legítima do proprietário.\033[0m")
        return True
    except BadSignatureError:
        print("\n\033[91m[ALERTA CRÍTICO] Falha na Assinatura! Transação fraudulenta detectada.\033[0m")
        return False

# Teste 1: Validando a transação legítima
verificar_autenticidade(dados_transacao, assinatura, chave_publica)

# Teste 2: Simulando um ataque de falsificação (Modificando o valor da transferência)
dados_adulterados = "Origem: Carteira_A | Destino: Carteira_B | Valor: 1000.0 BTC"
print(f"\n[!] Hacker tentando injetar transação adulterada: '{dados_adulterados}'")
verificar_autenticidade(dados_adulterados, assinatura, chave_publica)
