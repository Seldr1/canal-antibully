from flask import Flask, request, render_template_string
import datetime
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Canal Anônimo Contra Bullying</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial; background:#f4f4f4; padding:20px;">
    <h2>Canal Anônimo Contra Bullying</h2>
    <form method="POST">
        <textarea name="relato" rows="6" style="width:100%; padding:10px;" placeholder="Escreva seu relato aqui..." required></textarea><br><br>
        <button style="padding:10px 20px; background:#007bff; color:white; border:none; border-radius:5px;">
            Enviar Relato
        </button>
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
