import ast
import operator
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

OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}

def calcular(no):
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
        return no.value
    if isinstance(no, ast.BinOp) and type(no.op) in OPERADORES:
        return OPERADORES[type(no.op)](calcular(no.left), calcular(no.right))
    if isinstance(no, ast.UnaryOp) and type(no.op) in OPERADORES:
        return OPERADORES[type(no.op)](calcular(no.operand))
    raise ValueError("Expressão não permitida pela Força")

@app.route("/forca")
def forca():
    expressao = request.args.get("exp")
    try:
        return str(calcular(ast.parse(expressao, mode="eval").body))
    except (SyntaxError, ValueError, ZeroDivisionError):
        return "Expressão inválida", 400

@app.route("/aliados")
def aliados():
    r = requests.get("https://aliados.rebeldes.org/lista", verify=True)
    return r.text

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
