# Arquitetura de Rede e Fluxo do Ecossistema

Este documento descreve o fluxo de tráfego, as interações de rede e os mecanismos de segurança ativa implementados em nosso ecossistema descentralizado de auditoria e monitoramento de Blockchain.

## Visão Geral da Infraestrutura

O sistema opera sob uma arquitetura de microsserviços e segurança defensiva dividida em três camadas principais:
1. **Camada de Borda (Edge/Reverse Proxy):** Controlada pelo Nginx, atuando como o primeiro ponto de contato e escudo de rede.
2. **Camada de Monitoramento & Resposta (SIEM Local):** Gerenciada de forma contínua pelo script em Shell `sentinela.sh`.
3. **Camada de Lógica & Criptografia (Core Python):** Executada de forma isolada dentro do ambiente virtual `(.venv-auditoria)`.

---

## Fluxo de Dados e Interações de Rede

```text
[ Atacante / Usuário ]
          │ (Requisição HTTP/HTTPS)
          ▼
┌────────────────────────────────────────────────────────┐
│               PORTA 1337: PROXY REVERSO (Nginx)        │
├────────────────────────────────────────────────────────┤
│ 1. Rate Limiting (Máx 5 req/s) ──► Bloqueia com 503    │
│ 2. Escrita de eventos em Tempo Real no access.log      │
└─────────────────────────┬──────────────────────────────┘
                          │ (Geração de logs)
                          ▼
┌────────────────────────────────────────────────────────┐
│           CAMADA DE AUDITORIA: sentinela.sh           │
├────────────────────────────────────────────────────────┤
│ 1. Leitura contínua (`tail -F`) do arquivo de logs     │
│ 2. Rotação de armazenamento automatizada (.tar.gz)     │
│ 3. Filtro comportamental de ameaças (Cenários 1,2,3)   │
│ 4. Mitigação Ativa: Execução de bans automáticos via UFW│
│ 5. Sinalização Sonora Real (Hardware Beep/Audio)       │
└─────────────────────────┬──────────────────────────────┘
                          │ (Disparo de Alertas POST)
                          ▼
┌────────────────────────────────────────────────────────┐
│   PORTA 5000: API CENTRAL DE SEGURANÇA (Flask HTTPS)   │
├────────────────────────────────────────────────────────┤
│ 1. Tunelamento seguro com chaves criptográficas SSL    │
│ 2. Armazenamento persistente de incidentes em SQLite3  │
│ 3. Renderização dinâmica do Dashboard Web HTML         │
└────────────────────────────────────────────────────────┘
```

---

## Vetores de Mitigação Ativa e Segurança de Dados

### 1. Prevenção de Negação de Serviço (DoS/DDoS)
A diretiva `limit_req_zone` aplicada globalmente no Nginx analisa o endereço binário remoto do cliente (`$binary_remote_addr`). Se o tráfego originado por um único IP exceder 5 requisições por segundo, as conexões excedentes serão descartadas com erro HTTP 503, protegendo o processamento do nó Blockchain.

### 2. Controle de Integridade Local (HIDS)
O script `hids_criptografado.py` calcula hashesSHA-256 dos binários de produção e salva a base em formato criptografado usando criptografia simétrica AES/Fernet de 128 bits. Isso impede que atacantes adulterem as tabelas de referência para camuflar arquivos maliciosos.

### 3. Autenticidade e Privacidade de Transações
- **ECDSA (SECP256k1):** Garante o não-repúdio e a autoria das transações de criptoativos, validando as chaves assimétricas antes da inserção na rede.
- **RSA (2048-bit):** Utiliza criptografia de chaves públicas com preenchimento OAEP/SHA-256 para envelopar dados confidenciais das transferências operacionais, mantendo o payload confidencial durante o transporte.
