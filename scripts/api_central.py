from flask import Flask, request, jsonify, render_template_string
import time
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "siem_alertas.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                origem TEXT,
                nivel TEXT,
                mensagem TEXT
            )
        """)
        conn.commit()

# Inicializa o banco de dados se não existir
init_db()

HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title> SIEM CENTRAL - OPERAÇÕES BLOCKCHAIN</title>
    <style>
        body { background-color: #0d0f12; color: #cbd5e1; font-family: 'Courier New', monospace; padding: 30px; }
        h1 { color: #38bdf8; border-bottom: 2px solid #1e293b; padding-bottom: 10px; }
        .card { background-color: #1e293b; border-radius: 6px; padding: 15px; margin-bottom: 12px; border-left: 5px solid #64748b; }
        .WARNING { border-left-color: #eab308; }
        .CRITICAL { border-left-color: #ef4444; }
        .EMERGENCY { border-left-color: #dc2626; background-color: #2d1616; }
        .tag { font-weight: bold; padding: 2px 6px; border-radius: 4px; background: #0f172a; font-size: 12px; }
        .time { color: #94a3b8; float: right; font-size: 12px; }
    </style>
    <meta http-equiv="refresh" content="5">
</head>
<body>
    <h1> Painel de Incidentes Operacionais (SIEM + SQLite)</h1>
    <hr style="border: 1px solid #1e293b; margin-bottom: 20px;">
    {% for inc in incidentes %}
        <div class="card {{ inc[3] }}">
            <span class="time"> {{ inc[1] }}</span>
            <span class="tag" style="color:#38bdf8;"> {{ inc[2] }}</span>
            <span class="tag" style="color:white;">⚠️{{ inc[3] }}</span>
            <p style="margin-top: 10px; font-size: 15px;">{{ inc[4] }}</p>
        </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/dashboard', methods=['GET'])
def renderizar_dashboard():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM incidentes ORDER BY id DESC")
        alertas = cursor.fetchall()
    return render_template_string(HTML_DASHBOARD, incidentes=alertas), 200

@app.route('/alertas', methods=['POST'])
def receber_alerta():
    dados = request.get_json()
    if not dados or 'origem' not in dados or 'nivel' not in dados or 'mensagem' not in dados:
        return jsonify({"erro": "Payload inválido"}), 400
        
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO incidentes (timestamp, origem, nivel, mensagem) VALUES (?, ?, ?, ?)",
                       (ts, dados['origem'], dados['nivel'].upper(), dados['mensagem']))
        conn.commit()
    return jsonify({"status": "salvo_no_sqlite"}), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, ssl_context=('cert.pem', 'key.pem'))
