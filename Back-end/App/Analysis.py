# ============================================================
# === Analysis.py — Análise de Dados, Relatórios e Simulação ===
# ============================================================

import os
import csv
import shutil
import sqlite3
from datetime import datetime
from twilio.rest import Client

from App.Database import get_connection
from App.Utils import parse_date, format_currency
from App.Config import obter_meta_total, obter_whatsapp, TWILIO_SID, TWILIO_TOKEN

# ============================================================
# === Caminhos e inicialização ===
# ============================================================

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
DB_PATH = os.path.join(DATA_DIR, "yourcontrol.db")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# ============================================================
# === BACKUP AUTOMÁTICO ===
# ============================================================

def criar_backup_automatico():
    if os.path.exists(DB_PATH):
        agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_nome = f"backup_{agora}.db"
        backup_caminho = os.path.join(BACKUP_DIR, backup_nome)
        shutil.copy2(DB_PATH, backup_caminho)
        print(f"🗂️ Backup automático criado: {backup_nome}\n")
    else:
        print("ℹ️ Nenhum banco encontrado para backup.\n")


# ============================================================
# === RELATÓRIO LOCAL ===
# ============================================================

def gerar_relatorio(exportar=False):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM produtos")
    except sqlite3.OperationalError:
        print("❌ Tabela 'produtos' não encontrada. Cadastre um produto primeiro.\n")
        conn.close()
        return

    produtos = cursor.fetchall()
    conn.close()

    meta_total = obter_meta_total()
    total_lucro = 0
    ranking = []

    for p in produtos:
        idp, nome, entrada, saida, preco_compra, preco_venda, validade = p
        lucro_prod = (preco_venda - preco_compra) * saida
        total_lucro += lucro_prod
        ranking.append((nome, lucro_prod, validade))

    ranking.sort(key=lambda x: x[1], reverse=True)

    print("\n=== RELATÓRIO YOURCONTROL ===")
    print(f"💰 Lucro total atual: {format_currency(total_lucro)}")
    print(f"🎯 Meta total: {format_currency(meta_total)}")
    print(f"📉 Faltam: {format_currency(max(0, meta_total - total_lucro))} para atingir a meta\n")

    print("🏆 Produtos que mais geraram lucro:")
    for nome, valor, validade in ranking[:5]:
        aviso = ""
        if validade:
            dt = parse_date(validade)
            if dt:
                dias = (dt - datetime.now()).days
                if dias < 0:
                    aviso = " (⚠️ Vencido)"
                elif dias <= 7:
                    aviso = f" (⚠️ Vence em {dias} dias)"
        print(f"  - {nome}: {format_currency(valor)}{aviso}")

    print("-" * 50)

    if exportar:
        arquivo_csv = os.path.join(BASE_DIR, "relatorio_yourcontrol.csv")
        with open(arquivo_csv, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Produto", "Lucro", "Validade"])
            for nome, valor, validade in ranking:
                writer.writerow([nome, valor, validade or ""])
        print(f"✅ Relatório exportado: {arquivo_csv}\n")


# ============================================================
# === ENVIO VIA WHATSAPP (Twilio) ===
# ============================================================

def enviar_relatorio_whatsapp():
    numero = obter_whatsapp()
    if not numero:
        print("⚠️ Nenhum número de WhatsApp cadastrado.\n")
        return

    to_whatsapp = f"whatsapp:+55{numero.strip().replace('+55', '')}"
    from_whatsapp = "whatsapp:+14155238886"  # número padrão Twilio Sandbox

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, preco_compra, preco_venda, validade, entrada, saida FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    if not produtos:
        print("⚠️ Nenhum produto cadastrado.\n")
        return

    meta = obter_meta_total()
    lucro_total = sum((pv - pc) * saida for _, pc, pv, _, _, saida in produtos)

    produtos_vencendo = [nome for nome, _, _, val, _, _ in produtos
                         if val and (datetime.strptime(val, "%Y-%m-%d") - datetime.now()).days <= 3]
    mais_vendidos = sorted(produtos, key=lambda x: x[5], reverse=True)[:3]

    mensagem = (
        f"*📊 Relatório YourControl — {datetime.now().strftime('%d/%m/%Y')}*\n\n"
        f"💰 *Lucro atual:* {format_currency(lucro_total)}\n"
        f"🎯 *Meta total:* {format_currency(meta)}\n"
    )

    if lucro_total >= meta:
        mensagem += "✅ *Meta atingida!* Excelente resultado!\n\n"
    else:
        restante = meta - lucro_total
        mensagem += f"📉 Faltam *{format_currency(restante)}* para atingir sua meta.\n\n"

    mensagem += "🏆 *Top 3 produtos com mais saída:*\n"
    for nome, _, _, _, _, saida in mais_vendidos:
        mensagem += f" • {nome}: {saida} vendas\n"

    if produtos_vencendo:
        mensagem += "\n⚠️ *Produtos próximos da validade:*\n"
        for nome in produtos_vencendo:
            mensagem += f" • {nome}\n"

    mensagem += "\n📈 Continue acompanhando com *YourControl*! 🚀"

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(from_=from_whatsapp, body=mensagem, to=to_whatsapp)
        print("✅ Relatório enviado com sucesso via WhatsApp!\n")
    except Exception as e:
        print(f"❌ Erro ao enviar relatório: {e}\n")


# ============================================================
# === SUGESTÃO DE PREÇOS ===
# ============================================================

def sugestao_precos_para_meta():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, preco_compra, preco_venda, saida FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    meta = obter_meta_total()
    if not produtos:
        print("⚠️ Nenhum produto cadastrado.\n")
        return

    lucro_atual = sum((pv - pc) * saida for _, pc, pv, saida in produtos)
    falta = meta - lucro_atual

    if falta <= 0:
        print("🎉 Parabéns! Sua meta já foi atingida ou ultrapassada.\n")
        return

    if lucro_atual <= 0:
        print("⚠️ Não é possível sugerir preços — lucro atual é zero ou negativo.\n")
        return

    aumento_percentual = falta / lucro_atual
    print("\n=== SUGESTÃO DE AJUSTE DE PREÇOS ===")
    print(f"Lucro atual: {format_currency(lucro_atual)}")
    print(f"Meta total: {format_currency(meta)}")
    print(f"Falta: {format_currency(falta)} → aumento médio necessário: {aumento_percentual*100:.1f}%\n")

    print("💡 Sugestão de novos preços:")
    for nome, pc, pv, saida in produtos:
        novo_preco = pv * (1 + aumento_percentual)
        print(f" - {nome}: de {format_currency(pv)} → sugerido {format_currency(novo_preco)}")

    print("\n⚠️ Ajuste os preços com cuidado — considere o mercado.\n")


# ============================================================
# === SIMULADOR FINANCEIRO ===
# ============================================================

def simulador_financeiro():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, preco_compra, preco_venda, saida FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    if not produtos:
        print("⚠️ Nenhum produto cadastrado.\n")
        return

    lucro_atual = sum((pv - pc) * saida for _, pc, pv, saida in produtos)
    meta = obter_meta_total()

    print("\n=== SIMULADOR FINANCEIRO ===")
    print(f"💰 Lucro atual: {format_currency(lucro_atual)}")
    print(f"🎯 Meta total:  {format_currency(meta)}\n")

    print("O que deseja simular?")
    print("1️⃣ Lucro adicional desejado (R$)")
    print("2️⃣ Aumento percentual de preços (%)")
    print("3️⃣ Aumento percentual de vendas (%)")
    print("0️⃣ Voltar\n")

    opc = input("Escolha uma opção: ").strip()

    if opc == '1':
        try:
            adicional = float(input("Quanto deseja lucrar a mais (R$)? "))
        except ValueError:
            print("Valor inválido.\n")
            return

        if lucro_atual <= 0:
            print("⚠️ Não é possível simular aumento de lucro, pois o lucro atual é zero ou negativo.\n")
            return

        novo_lucro = lucro_atual + adicional
        aumento = adicional / lucro_atual

        print(f"\n📈 Para lucrar {format_currency(adicional)} a mais, é necessário aumentar os preços em cerca de {aumento*100:.1f}%.\n")
        for nome, pc, pv, saida in produtos:
            novo_preco = pv * (1 + aumento)
            print(f" - {nome}: {format_currency(pv)} → {format_currency(novo_preco)}")
        print()

    elif opc == '2':
        try:
            aumento = float(input("Aumentar preços em quantos %? ")) / 100
        except ValueError:
            print("Valor inválido.\n")
            return

        novo_lucro = sum(((pv * (1 + aumento)) - pc) * saida for _, pc, pv, saida in produtos)
        print(f"\n💰 Novo lucro estimado: {format_currency(novo_lucro)}")
        print(f"Aumento estimado: {format_currency(novo_lucro - lucro_atual)}\n")

    elif opc == '3':
        try:
            aumento = float(input("Vendas aumentarão em quantos %? ")) / 100
        except ValueError:
            print("Valor inválido.\n")
            return

        novo_lucro = sum((pv - pc) * (saida * (1 + aumento)) for _, pc, pv, saida in produtos)
        print(f"\n📊 Novo lucro estimado: {format_currency(novo_lucro)}")
        print(f"Aumento estimado: {format_currency(novo_lucro - lucro_atual)}\n")

    elif opc == '0':
        print("Voltando ao menu...\n")
        return

    else:
        print("Opção inválida.\n")