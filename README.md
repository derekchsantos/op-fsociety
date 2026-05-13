# Sentinela: Monitoramento & Auditoria Operacional para Redes Blockchain

Este projeto implementa uma solução leve e robusta de **resposta a incidentes e auditoria de infraestrutura** automatizada via Shell Script. Ele foi projetado para atuar em conjunto com um proxy reverso (Nginx) para mitigar ameaças, ataques de negação de serviço (DoS) e monitorar a saúde operacional de nós (nodes) em redes Blockchain de produção.

## Funcionalidades Operacionais

- **Monitoramento de Logs em Tempo Real:** Escuta contínua das requisições direcionadas à API RPC e endpoints da Blockchain.
- **Detecção de Incidentes Críticos:** Identificação imediata de erros de gateway (`502 Bad Gateway` / `504 Gateway Timeout`), sinalizando queda do nó Blockchain.
- **Auditoria de Segurança:** Alertas visuais e registros instantâneos ao detectar tentativas de varredura ou acessos não autorizados a rotas sensíveis (`/wallet`, `/admin`, `/rpc/private`).
- **Gerenciamento Inteligente de Armazenamento:** Rotação automática de logs com compactação `.tar.gz` ao atingir limites de espaço (prevenindo preenchimento total do disco).
- **Proteção do Script:** Arquitetura pronta para compilação e criptografia do código-fonte através do `shc` para execução segura em servidores.

## Tecnologias Utilizadas

- **Shell Script (Bash):** Lógica central de automação e manipulação de fluxos de dados em tempo real.
- **Nginx:** Proxy reverso e servidor web monitorado.
- **Git & GitHub:** Versionamento de código e boas práticas de exclusão com `.gitignore`.
- **Ambiente Isolado:** Homologado utilizando infraestrutura Linux em conjunto com ambientes virtuais Python (`venv`).

## Estrutura de Arquivos Recomendada

```text
├── backups_auditoria/       # Diretório gerenciado para armazenar backups compactados
├── sentinela.sh             # Script original de automação (Criação/Desenvolvimento)
├── sentinela.sh.x           # Executável criptografado de produção (Gerado via SHC)
├── .gitignore               # Proteção de vazamento de logs e ambientes isolados
└── README.md                # Documentação técnica do projeto
```

## Como Executar o Ambiente

1. Certifique-se de dar permissão de execução ao script:
   ```bash
   chmod +x sentinela.sh
   ```

2. Inicialize o monitor em background ou em uma sessão dedicada:
   ```bash
   ./sentinela.sh
   ```

