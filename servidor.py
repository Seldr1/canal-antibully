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
    except:
        conteudo = "Nenhum relato ainda."
    return f"<pre>{conteudo}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
