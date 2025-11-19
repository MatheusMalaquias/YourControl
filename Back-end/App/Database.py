import json
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "produtos.json"))
META_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "meta.json"))

# garante as pastas
if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))

# cria arquivos caso não existam
if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        json.dump([], f)

if not os.path.exists(META_PATH):
    with open(META_PATH, "w") as f:
        json.dump({"meta_percentual": 0}, f)


def load_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_meta():
    with open(META_PATH, "r") as f:
        return json.load(f)


def save_meta(data):
    with open(META_PATH, "w") as f:
        json.dump(data, f, indent=4)