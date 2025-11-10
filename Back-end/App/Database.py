import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'Data')
DB_PATH = os.path.join(DB_DIR, 'yourcontrol.db')

def get_connection():
    """Conecta ao banco SQLite e cria tabelas se necessário."""
    if not os.path.isdir(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        entrada REAL NOT NULL DEFAULT 0,
        saida REAL NOT NULL DEFAULT 0,
        preco_compra REAL NOT NULL DEFAULT 0,
        preco_venda REAL NOT NULL DEFAULT 0,
        validade TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        quantidade REAL NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes (
        chave TEXT PRIMARY KEY,
        valor TEXT
    )
    """)

    conn.commit()
    return conn