import sqlite3
import subprocess
import requests
from flask import Flask, request

app = Flask(__name__)

API_KEY = "AKIAIOSFODNN7EXAMPLE"
DB_PASSWORD = "senha_do_imperador_123"

@app.route("/porta-termica")
def porta_termica():
    alvo = request.args.get("alvo")
    conn = sqlite3.connect("rebeldes.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM pilotos WHERE nome = ?", (alvo,))
    return str(cur.fetchall())

COMANDOS_PERMITIDOS = {
    "data": ["date"],
    "uptime": ["uptime"],
}

@app.route("/holocron")
def holocron():
    comando = request.args.get("cmd")
    for nome, argumentos in COMANDOS_PERMITIDOS.items():
        if comando == nome:
            return subprocess.check_output(argumentos)
    return "Comando não permitido pelo Holocron", 400

@app.route("/forca")
def forca():
    expressao = request.args.get("exp")
    return str(eval(expressao))

@app.route("/aliados")
def aliados():
    r = requests.get("https://aliados.rebeldes.org/lista", verify=False)
    return r.text

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
