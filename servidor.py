from flask import Flask, request, render_template_string, redirect
import datetime
import os

app = Flask(__name__)

# =========================
# CONFIGURAÇÕES
# =========================

SENHA_ADMIN = "2103"  # <-- MUDE ISSO

# =========================
# PÁGINA DE ENVIO
# =========================

FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Canal Seguro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            font-family: Arial;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background: #1e293b;
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        textarea {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: none;
            resize: none;
        }
        button {
            width: 100%;
            padding: 12px;
            margin-top: 15px;
            background: #38bdf8;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
        }
        .msg {
            text-align: center;
            margin-top: 10px;
            color: #22c55e;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Canal Anônimo 💙</h2>
        <form method="POST">
            <textarea name="relato" rows="5" placeholder="Escreva seu relato..." required></textarea>
            <button type="submit">Enviar Relato</button>
        </form>
        {% if enviado %}
        <div class="msg">Relato enviado com sucesso ✅</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    enviado = False
    if request.method == "POST":
        relato = request.form["relato"]
        with open("relatos.txt", "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.datetime.now()} ---\n")
            f.write(relato + "\n")
        enviado = True
    return render_template_string(FORM_HTML, enviado=enviado)

# =========================
# LOGIN ADMIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == SENHA_ADMIN:
            return redirect("/painel")
        else:
            return "<h3>Senha incorreta ❌</h3>"

    return """
    <h2>Login Admin</h2>
    <form method="POST">
        <input type="password" name="senha" placeholder="Senha" required>
        <button type="submit">Entrar</button>
    </form>
    """

# =========================
# PAINEL PROTEGIDO
# =========================

@app.route("/painel")
def painel():
    try:
        with open("relatos.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
            relatos = conteudo.split("---")
    except:
        relatos = []

    html = """
    <h1>Painel de Relatos</h1>
    <form action="/apagar" method="POST">
        <button style='background:red;color:white;'>Apagar Todos</button>
    </form>
    <hr>
    """

    contador = 0

    for r in relatos:
        if r.strip():
            contador += 1
            html += f"<pre>{r}</pre><hr>"

    html += f"<p>Total: {contador} relatos</p>"

    return html

# =========================
# APAGAR RELATOS
# =========================

@app.route("/apagar", methods=["POST"])
def apagar():
    open("relatos.txt", "w").close()
    return redirect("/painel")

# =========================
# CONFIGURAÇÃO RENDER
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
