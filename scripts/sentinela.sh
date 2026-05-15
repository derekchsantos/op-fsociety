#!/bin/bash
LOG_FILE="/var/log/nginx/access.log"
AUDIT_LOG="./auditoria_blockchain.log"
BACKUP_DIR="./backups_auditoria"
MAX_LINHAS=50

# Altera o arquivo de log para o diretório temporário caso não tenha permissão de escrita no padrão do Nginx
[ ! -w "$LOG_FILE" ] && LOG_FILE="/tmp/access.log"
touch "$LOG_FILE" 2>/dev/null

touch "$AUDIT_LOG" 2>/dev/null || AUDIT_LOG="/tmp/auditoria_blockchain.log"

echo -e "\e[32m[SENTINELA ATIVA]\e[0m Monitorando incidentes e gerenciando armazenamento..."
echo "[+] Lendo logs de: $LOG_FILE"
echo "[+] Gravando registros em: $AUDIT_LOG"
echo "--------------------------------------------------"

# Laço principal de leitura contínua em tempo real
tail -F "$LOG_FILE" | while read -r line; do
    HORA_ATUAL=$(date '+%Y-%m-%d %H:%M:%S')
    HORA_ARQUIVO=$(date '+%Y-%m-%d_%H-%M-%S')
    
    # ROTAÇÃO COM BACKUP COMPACTADO (.tar.gz)
    if [ -f "$AUDIT_LOG" ] && [ "$(wc -l < "$AUDIT_LOG")" -gt "$MAX_LINHAS" ]; then
        mkdir -p "$BACKUP_DIR"
        NOME_BACKUP="$BACKUP_DIR/backup_auditoria_$HORA_ARQUIVO.tar.gz"
        tar -czf "$NOME_BACKUP" "$AUDIT_LOG" 2>/dev/null
        echo "[$HORA_ATUAL] [INFO] Limpando arquivo antigo pós-backup." > "$AUDIT_LOG"
        echo -e "\e[34m[SISTEMA]\e[0m Limite atingido! Backup criado com sucesso: $NOME_BACKUP"
    fi

    # CENÁRIO 1: Erro 502/504 (Blockchain fora do ar)
    if echo "$line" | grep -qE " 502 | 504 "; then
        IP=$(echo "$line" | awk '{print $1}')
        ROTA=$(echo "$line" | awk '{print $7}')
        
        echo -e "\e[31m[INCIDENTE CRÍTICO]\e[0m API da Blockchain fora do ar! IP: $IP | Rota: $ROTA"
        echo "[$HORA_ATUAL] [CRITICAL] Blockchain Offline - Origem IP: $IP - Rota: $ROTA" >> "$AUDIT_LOG"
        
        # Alerta sonoro do Cenário 1
        beep -f 1000 -l 500 2>/dev/null || (speaker-test -t sine -f 1000 -l 1 & PID=$!; sleep 0.3; kill $PID) 2>/dev/null
    fi

    # CENÁRIO 2: Acesso a rotas administrativas ou carteiras
    if echo "$line" | grep -qE "admin|rpc/private|wallet"; then
        IP=$(echo "$line" | awk '{print $1}')
        ROTA=$(echo "$line" | awk '{print $7}')
        
        echo -e "\e[33m[ALERTA DE AUDITORIA]\e[0m Rota sensível acessada! IP: $IP | Rota: $ROTA"
        echo "[$HORA_ATUAL] [WARNING] Tentativa de Acesso Sensivel - Origem IP: $IP - Rota: $ROTA" >> "$AUDIT_LOG"
        
        # OPERAÇÃO FIREWALL: Bloqueia o IP invasor automaticamente se ele não for o Localhost
        if [ "$IP" != "127.0.0.1" ] && [ "$IP" != "localhost" ]; then
            echo -e "\e[41m[MITIGAÇÃO ATIVA]\e[0m Bloqueando IP $IP no Firewall do Linux..."
            sudo ufw deny from "$IP" to any comment 'Sentinela: Tentativa de invasao na Blockchain' 2>/dev/null
        else
            echo -e "\e[34m[SISTEMA]\e[0m Origem é Localhost. Pulando regra de bloqueio do Firewall para evitar auto-ban."
        fi
    fi

    # CENÁRIO 3: Fraude detectada pelo script de auditoria em Python
    if echo "$line" | grep -q "blockchain/fraud"; then
        echo -e "\e[41m\e[37m[🚨 ALERTA MÁXIMO]\e[0m INTEGRIDADE DA BLOCKCHAIN VIOLADA!"
        echo "[$HORA_ATUAL] [EMERGENCY] Fraude detectada no bloco!" >> "$AUDIT_LOG"
        
        # Sequência de bipes rápidos de emergência do Cenário 3
        for i in {1..3}; do 
            beep -f 2000 -l 150 2>/dev/null || (speaker-test -t sine -f 2000 -l 1 & P=$!; sleep 0.1; kill $P) 2>/dev/null
            sleep 0.1
        done
    fi
done
