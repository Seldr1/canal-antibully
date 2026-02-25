from flask import Flask, request, render_template_string
import datetime
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Canal Anônimo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial; padding:20px;">
    <h2>Canal Anônimo Contra Bullying</h2>
    <form method="POST">
        <textarea name="relato" rows="6" style="width:100%;" required></textarea><br><br>
        <button>Enviar Relato</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        relato = request.form["relato"]
        with open("relatos.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.datetime.now()} ---\n")
            f.write(relato + "\n")
    return render_template_string(HTML)

# 🔐 ROTA ADMIN

@app.route("/admin")
def admin():
    try:
        with open("relatos.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
            relatos = conteudo.split("---")
    except:
        relatos = []

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Painel Admin</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: white;
                padding: 20px;
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
            }
            .card {
                background: #1e293b;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                box-shadow: 0 0 10px rgba(0,0,0,0.4);
            }
            .data {
                font-size: 12px;
                color: #38bdf8;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>📋 Painel de Relatos</h1>
    """

    for r in relatos:
        if r.strip():
            html += f"""
            <div class="card">
                <div class="data">{r.splitlines()[0]}</div>
                <div>{'<br>'.join(r.splitlines()[1:])}</div>
            </div>
            """

    html += "</body></html>"
    return html

