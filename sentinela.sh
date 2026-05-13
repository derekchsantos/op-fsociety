#!/bin/bash
LOG_FILE="/var/log/nginx/access.log"
AUDIT_LOG="./auditoria_blockchain.log"
BACKUP_DIR="./backups_auditoria"
MAX_LINHAS=50

touch "$AUDIT_LOG" 2>/dev/null || AUDIT_LOG="/tmp/auditoria_blockchain.log"

echo -e "\e[32m[SENTINELA ATIVA]\e[0m Monitorando incidentes e gerenciando armazenamento..."
echo "[+] Gravando registros em: $AUDIT_LOG"
echo "--------------------------------------------------"

tail -F "$LOG_FILE" | while read -r line; do
    HORA_ATUAL=$(date '+%Y-%m-%d_%H-%M-%S')
    
    # ROTAÇÃO COM BACKUP COMPACTADO (.tar.gz)
    if [ -f "$AUDIT_LOG" ] && [ "$(wc -l < "$AUDIT_LOG")" -gt "$MAX_LINHAS" ]; then
        mkdir -p "$BACKUP_DIR"
        NOME_BACKUP="$BACKUP_DIR/backup_auditoria_$HORA_ATUAL.tar.gz"
        
        # Compacta o log atual e zera o arquivo original
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
    fi

    # CENÁRIO 2: Acesso a rotas administrativas ou carteiras
    if echo "$line" | grep -qE "admin|rpc/private|wallet"; then
        IP=$(echo "$line" | awk '{print $1}')
        ROTA=$(echo "$line" | awk '{print $7}')
        echo -e "\e[33m[ALERTA DE AUDITORIA]\e[0m Rota sensível acessada! IP: $IP | Rota: $ROTA"
        echo "[$HORA_ATUAL] [WARNING] Tentativa de Acesso Sensivel - Origem IP: $IP - Rota: $ROTA" >> "$AUDIT_LOG"
    fi
done
