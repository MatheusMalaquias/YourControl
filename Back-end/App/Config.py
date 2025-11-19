import json
import os

META_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "meta.json"))

if not os.path.exists(META_PATH):
    with open(META_PATH, "w") as f:
        json.dump({"meta": 0, "whatsapp": ""}, f)

def load_meta():
    with open(META_PATH, "r") as f:
        return json.load(f)

def save_meta(data):
    with open(META_PATH, "w") as f:
        json.dump(data, f, indent=4)

def definir_meta_total():
    meta = float(input("Meta total de lucro: "))
    data = load_meta()
    data["meta"] = meta
    save_meta(data)
    print("Meta salva!\n")

def definir_whatsapp():
    numero = input("Número do WhatsApp (somente números): ")
    data = load_meta()
    data["whatsapp"] = numero
    save_meta(data)
    print("Número salvo!\n")