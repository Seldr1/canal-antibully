print("=== RELATOS RECEBIDOS ===\n")

try:
    with open("relatos.txt", "r", encoding="utf-8") as f:
        print(f.read())
except:
    print("Nenhum relato recebido ainda.")