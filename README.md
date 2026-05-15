# Sentinela: Monitoramento, Auditoria & Segurança Criptográfica para Blockchain

Este repositório consolida um ecossistema integrado de **Segurança Defensiva, Criptografia Avançada e Resposta a Incidentes**, projetado especificamente para mitigar ameaças, auditar integridade de dados e proteger a infraestrutura de redes Blockchain de produção.

## Módulos Implementados

### 1. Camada de Rede & Proxy Reverso (`Nginx`)
- **Rate Limiting Ativo:** Configurado para restringir abusos na camada de rede, limitando requisições na porta `1337` a 5 acessos por segundo por IP (mitigação de DoS).
- **Proteção de Gateway:** Resposta estruturada para erros de comunicação interna (`502`/`504`).

### 2. Monitoramento de Borda (`/scripts/sentinela.sh`)
- **Análise em Tempo Real:** Captura de eventos contínuos via logs de tráfego, isolando IPs invasores e rotas sensíveis em menos de 1 segundo.
- **Mitigação Ativa com Firewall:** Bloqueio automatizado de IPs agressores via regras do Linux `UFW`.
- **Sinalização Sonora e Rotação:** Emissão de alertas físicos via hardware (`beep`) e compactação automática de logs em `.tar.gz` para controle de disco.

### 3. API Centralizadora SIEM (`/scripts/api_central.py`)
- **Tunelamento HTTPS/TLS:** Comunicação cifrada ponta a ponta usando certificados SSL/TLS autoassinados (`X.509 RSA 4096-bit`).
- **Persistência de Logs:** Banco de dados relacional incorporado em `SQLite3` para retenção permanente de auditoria.
- **Dashboard Web:** Interface gráfica em tempo real renderizada de forma nativa para controle de incidentes.

### 4. Núcleo Criptográfico & Auditoria (`/scripts/`)
- **`cripto_transacao.py`:** Autenticidade e não-repúdio de transferências utilizando chaves assimétricas **ECDSA** (Curva Criptográfica `SECP256k1`).
- **`cripto_rsa.py`:** Privacidade de payloads confidenciais trafegados em redes públicas através de envelopamento **RSA 2048-bit** com preenchimento OAEP/SHA-256.
- **`hids_criptografado.py`:** Sistema HIDS local que audita binários críticos e salva a base de assinaturas cifrada de forma simétrica com **AES/Fernet**.
- **`anti_bruteforce.py`:** Algoritmo comportamental de detecção de ataques de força bruta em painéis de gerência.
- **`smart_contract_multisig.py`:** Mecanismo de governança descentralizada baseada em regras 2-de-2 (M-of-N Multi-signatures) utilizando chaves SECP256k1 para travar a movimentação de fundos corporativos.
- **`blindar_banco.py`:** Algoritmo de segurança física em disco que cifra a base de dados relacional inteira do SQLite utilizando envelopes AES-128 em períodos de inatividade.
- **`seguranca_geografica.py`:** Módulo comportamental de Whitelist e análise de telemetria geográfica contra ataques de falsificação de IPs em validadores de rede.
- **`pentest_sqli.py`:** Ferramenta ofensiva usada para validar a resiliência da infraestrutura contra ataques de injeção de código.

## Organização do Repositório

```text
├── scripts/
│   ├── api_central.py           # SIEM Flask com persistência SQLite e TLS
│   ├── sentinela.sh             # Core daemon de monitoramento e mitigação UFW
│   ├── auditoria_blockchain.py   # Monitor de fraudes na cadeia de blocos
│   ├── hids_criptografado.py    # Detector de intrusão local com hashes AES
│   ├── cripto_transacao.py      # Assinatura digital de carteiras ECDSA
│   ├── cripto_rsa.py            # Criptografia assimétrica de payloads
│   ├── anti_bruteforce.py       # Filtro comportamental de requisições
│   └── evidencia_operacional.txt# Relatório estático gerado pós-execução bem-sucedida
├── ARCHITECTURE.md              # Mapeamento do fluxo de rede e topologia
├── .gitignore                   # Exclusão de credenciais, chaves (.pem, .key) e db
└── README.md                    # Documentação principal do ecossistema
```

## Como Executar a Infraestrutura

1. Ative o ambiente virtual e execute a API Central (SIEM):
   ```bash
   python scripts/api_central.py
   ```
2. Inicialize o monitor de segurança em outra sessão do terminal:
   ```bash
   ./scripts/sentinela.sh
   ```
3. Realize testes automatizados de estresse utilizando o injetor de tráfego:
   ```bash
   python scripts/injetor_testes.py
   ```
