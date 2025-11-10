import os
import sqlite3
from dotenv import load_dotenv
from App.Database import get_connection

load_dotenv()

# === 1️⃣ META DE LUCRO TOTAL ===
def definir_meta_total():
    try:
        meta = float(input("Digite o valor da meta total de lucro (R$): ").replace(",", "."))
    except ValueError:
        print("❌ Valor inválido. Digite apenas números.\n")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)", ("meta_total", meta))
    conn.commit()
    conn.close()

    print(f"✅ Meta total de lucro definida: R$ {meta:,.2f}\n")


def obter_meta_total():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", ("meta_total",))
    row = cursor.fetchone()
    conn.close()
    return float(row[0]) if row else 0.0


# === 2️⃣ NÚMERO DO WHATSAPP ===
def definir_whatsapp():
    numero = input("Digite o número do WhatsApp (somente DDD e número, ex: 11987654321): ").strip()
    if not numero.isdigit() or len(numero) < 10:
        print("❌ Número inválido. Digite apenas números, com DDD.\n")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)", ("whatsapp", numero))
    conn.commit()
    conn.close()

    print(f"✅ Número de WhatsApp salvo: {numero}\n")


def obter_whatsapp():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", ("whatsapp",))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None