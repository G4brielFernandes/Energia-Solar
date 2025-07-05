from flask import Flask, render_template, request, jsonify
import backend
import lista
import sys
import os

# ✅ Ajuste de caminho quando roda .exe com PyInstaller
base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

template_dir = os.path.join(base_path, 'templates')
static_dir = os.path.join(base_path, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.json
    cidade = data["cidade"]
    kwh = float(data["kwh"])
    potencia = int(data["potencia"])
    resultado = backend.resultado(cidade, kwh, potencia)
    return jsonify(resultado)

@app.route("/personalizar", methods=["POST"])
def personalizar():
    data = request.json
    resultado_anterior = data["resultado_anterior"]
    modelo = data["modelo"]
    max_kwp = float(data["max_kwp"])
    resultado = backend.resultado_personalizado(resultado_anterior, modelo, max_kwp)
    return jsonify(resultado)

@app.route("/inversores")
def inversores():
    return jsonify(lista.inversores)

@app.route("/cidades")
def cidades():
    return jsonify(backend.cidades_disponiveis)

if __name__ == "__main__":
    # Só um run! O app.run() já inicia o servidor na porta 5000
    app.run(host="127.0.0.1", port=5000, debug=True)
