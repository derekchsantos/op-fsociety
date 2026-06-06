from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

print("[+] Inicializando Infraestrutura de Chaves Assimétricas (RSA 2048-bit)...")

# 1. Geração das chaves criptográficas
chave_privada_minerador = rsa.generate_private_key(public_exponent=65537, key_size=2048)
chave_publica_rede = chave_privada_minerador.public_key()

# 2. Dados confidenciais da transação que trafegará pela rede pública
payload_transacao = b"Transacao Privada: Whiterose enviou 500_000 E-Coin para Dark Army"

# 3. Criptografia com a Chave Pública (Qualquer usuário cifra, apenas o minerador decifra)
dados_cifrados = chave_publica_rede.encrypt(
    payload_transacao,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

print(f"\n Payload Criptografado (Bytes Cifrados): {dados_cifrados[:30]}...")

# 4. Descriptografia usando a Chave Privada correspondente
dados_reais = chave_privada_minerador.decrypt(
    dados_cifrados,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

print(f"\033[92m Sucesso! Payload descriptografado pelo Minerador: {dados_reais.decode()}\033[0m")
