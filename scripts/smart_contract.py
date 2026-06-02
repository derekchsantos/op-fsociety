# @author Derek Christopher
# -*- coding: utf-8 -*-

import hashlib
import json
import time
from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError
import base64
import requests

# Desabilita avisos de certificados autoassinados no terminal para manter o log limpo
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("Inicializando Engine de Smart Contracts com Integração SIEM...")

class SmartContractEscrow:
    def __init__(self, carteira_admin):
        self.admin = carteira_admin
        self.api_url = "https://127.0.0"
        self.ledgers_saldos = {
            "Carteira_Cliente": 500.0,
            "Carteira_Fornecedor": 50.0,
            "Contrato_Custodia": 0.0
        }
        print("[✓] Estado inicial da Ledger carregado.")

    def enviar_alerta_siem(self, nivel, mensagem):
        """ Envia um alerta estruturado via POST HTTPS para a API Central """
        payload = {
            "origem": "SmartContract-Engine",
            "nivel": nivel,
            "mensagem": mensagem
        }
        try:
            # Envia via HTTPS ignorando o certificado autoassinado local
            requests.post(self.api_url, json=payload, verify=False, timeout=2)
            print("Notificação de incidente enviada para a API Central.")
        except Exception:
            print("Erro de Comunicação: API Central offline. Alerta retido localmente.")

    def verificar_assinatura(self, dados_string, assinatura_b64, chave_publica_b64):
        try:
            ch_pub_bytes = base64.b64decode(chave_publica_b64)
            assin_bytes = base64.b64decode(assinatura_b64)
            chave_publica = VerifyingKey.from_string(ch_pub_bytes, curve=SECP256k1)
            return chave_publica.verify(assin_bytes, dados_string.encode('utf-8'))
        except (BadSignatureError, Exception):
            return False

    def executar_transacao_custodia(self, origem, destino, valor, assinatura, ch_publica):
        print(f"\n[+] Smart Contract acionado: {origem} ──► {destino} | Valor: {valor} BTC")
        
        # Regra 1: Validação de fundos disponíveis na Ledger
        if self.ledgers_saldos.get(origem, 0) < valor:
            msg_erro = f"Contrato REVERTIDO: {origem} tentou transferir {valor} BTC, mas possui apenas {self.ledgers_saldos.get(origem, 0)} BTC."
            print(f"\033[91m[-] {msg_erro}\033[0m")
            
            # GATILHO SIEM
            self.enviar_alerta_siem("WARNING", msg_erro)
            return False
            
        # Regra 2: Verificação de Autenticidade Criptográfica (Anti-Fraude)
        dados_verificacao = f"{origem}:{destino}:{valor}"
        if not self.verificar_assinatura(dados_verificacao, assinatura, ch_publica):
            msg_erro = f"Ataque detectado! Assinatura digital inválida ou falsificada na tentativa de envio de {valor} BTC para {destino}."
            print(f"\033[91m[-] {msg_erro}\033[0m")
            
            # GATILHO SIEM (Nível Máximo de Alerta)
            self.enviar_alerta_siem("EMERGENCY", msg_erro)
            return False
            
        # Execução legítima das cláusulas
        print("[*] Cláusulas atendidas. Movimentando ativos na Ledger...")
        self.ledgers_saldos[origem] -= valor
        self.ledgers_saldos["Contrato_Custodia"] += valor
        
        time.sleep(0.5)
        self.ledgers_saldos["Contrato_Custodia"] -= valor
        self.ledgers_saldos[destino] += valor
        print(f"Liquidação concluída com sucesso para {destino}.")
        return True

# --- FLUXO DE VERIFICAÇÃO OPERACIONAL ---
ch_privada_cliente = SigningKey.generate(curve=SECP256k1)
ch_publica_cliente = ch_privada_cliente.verifying_key
ch_pub_b64 = base64.b64encode(ch_publica_cliente.to_string()).decode()

dados_originais = "Carteira_Cliente:Carteira_Fornecedor:150.0"
assinatura_valida = base64.b64encode(ch_privada_cliente.sign(dados_originais.encode('utf-8'))).decode()

contrato = SmartContractEscrow(carteira_admin="Carteira_Admin_01")

print("\n--- TESTE 1: TENTATIVA DE QUEBRA DE REGRA DE SALDO ---")
contrato.executar_transacao_custodia("Carteira_Cliente", "Carteira_Fornecedor", 9999.0, assinatura_valida, ch_pub_b64)

print("\n--- TESTE 2: TENTATIVA DE QUEBRA DE INTEGRIDADE (FRAUDE) ---")
contrato.executar_transacao_custodia("Carteira_Cliente", "Carteira_Fornecedor", 150.0, "AssinaturaInvalidaAqui==", ch_pub_b64)
