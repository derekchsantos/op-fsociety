from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Banco de dados volátil em memória para armazenar o histórico do Dashboard
painel_incidentes = []

@app.route('/alertas', methods=['GET'])
def listar_alertas():
    # Retorna o histórico de incidentes para o administrador da rede
    return jsonify({"status": "operacional", "total_incidentes": len(painel_incidentes), "incidentes": painel_incidentes}), 200

@app.route('/alertas', methods=['POST'])
def receber_alerta():
    dados = request.get_json()
    
    if not dados or 'origem' not in dados or 'nivel' not in dados or 'mensagem' not in dados:
        return jsonify({"erro": "Payload mal formatado ou incompleto"}), 400
        
    novo_incidente = {
        "id": len(painel_incidentes) + 1,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "origem": dados['origem'],       # Ex: HIDS, ShellScript, PythonBlockchain
        "nivel": dados['nivel'].upper(),   # Ex: WARNING, CRITICAL, EMERGENCY
        "mensagem": dados['mensagem']
    }
    
    painel_incidentes.append(novo_incidente)
    
    # Exibição visual de emergência diretamente no terminal da API central
    cor_alerta = "\033[93m" if novo_incidente['nivel'] == "WARNING" else "\033[91m"
    print(f"{cor_alerta}[{novo_incidente['nivel']}] Incidente recebido de [{novo_incidente['origem']}]: {novo_incidente['mensagem']}\033[0m")
    
    return jsonify({"status": "registrado", "incidente_id": novo_incidente['id']}), 201

if __name__ == '__main__':
    print("[+] Inicializando SIEM Central da Blockchain...")
    # Executa a API localmente na porta de gerência operacional 5000
    app.run(host='127.0.0.1', port=5000, debug=False)
