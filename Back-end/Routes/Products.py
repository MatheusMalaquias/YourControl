from App.Database import get_connection
from App.Utils import parse_date
from datetime import datetime


# =============================
#  FUNÇÕES USADAS PELO TERMINAL
# =============================

def cadastrar_produto():
    conn = get_connection()
    cursor = conn.cursor()

    nome = input("Nome do produto: ").strip()
    if not nome:
        print("❌ Nome vazio. Cancelando cadastro.\n")
        return

    try:
        entrada = float(input("Quantidade comprada (kg/unid): ").strip() or 0)
        preco_compra = float(input("Preço de compra (R$): ").strip() or 0)
        preco_venda = float(input("Preço de venda (R$): ").strip() or 0)
        validade = input("Validade (AAAA-MM-DD) [opcional]: ").strip() or None
    except ValueError:
        print("⚠️ Entrada inválida.\n")
        return

    if validade and not parse_date(validade):
        print("⚠️ Formato de data inválido. Use AAAA-MM-DD.\n")
        return

    cursor.execute("""
        INSERT INTO produtos (nome, entrada, saida, preco_compra, preco_venda, validade)
        VALUES (?, ?, 0, ?, ?, ?)
    """, (nome, entrada, preco_compra, preco_venda, validade))
    conn.commit()
    conn.close()
    print(f"✅ Produto '{nome}' cadastrado com sucesso!\n")


def registrar_compra():
    conn = get_connection()
    cursor = conn.cursor()

    listar_produtos(True)
    try:
        idp = int(input("ID do produto: "))
        qtd = float(input("Quantidade comprada: "))
    except ValueError:
        print("⚠️ Entrada inválida.\n")
        return

    cursor.execute("SELECT entrada FROM produtos WHERE id=?", (idp,))
    row = cursor.fetchone()
    if not row:
        print("❌ Produto não encontrado.\n")
        return

    nova_entrada = row[0] + qtd
    cursor.execute("UPDATE produtos SET entrada=? WHERE id=?", (nova_entrada, idp))
    conn.commit()
    conn.close()
    print("✅ Compra registrada.\n")


def registrar_venda():
    conn = get_connection()
    cursor = conn.cursor()

    listar_produtos(True)
    try:
        idp = int(input("ID do produto vendido: "))
        qtd = float(input("Quantidade vendida: "))
    except ValueError:
        print("⚠️ Entrada inválida.\n")
        return

    cursor.execute("SELECT entrada, saida, nome FROM produtos WHERE id=?", (idp,))
    row = cursor.fetchone()
    if not row:
        print("❌ Produto não encontrado.\n")
        return

    entrada, saida_atual, nome = row
    if saida_atual + qtd > entrada:
        print("⚠️ Estoque insuficiente.\n")
        return

    nova_saida = saida_atual + qtd
    now = datetime.now().isoformat()
    cursor.execute("UPDATE produtos SET saida=? WHERE id=?", (nova_saida, idp))
    cursor.execute("INSERT INTO vendas (produto_id, quantidade, data) VALUES (?, ?, ?)", (idp, qtd, now))
    conn.commit()
    conn.close()
    print(f"💰 Venda registrada para {nome}.\n")


def listar_produtos(exibir_ids=False):
    conn = get_connection()
    cursor = conn.cursor()

    if exibir_ids:
        cursor.execute("SELECT id, nome, preco_venda, entrada, saida FROM produtos")
        produtos = cursor.fetchall()
        conn.close()

        if not produtos:
            print("⚠️ Nenhum produto cadastrado.\n")
            return

        print("\n=== LISTA DE PRODUTOS ===")
        print(f"{'ID':<5} | {'Produto':<20} | {'Valor de Venda':<15} | {'Estoque':<10}")
        print("-" * 60)

        for idp, nome, preco_venda, entrada, saida in produtos:
            estoque = entrada - saida
            print(f"{idp:<5} | {nome:<20} | R${preco_venda:<14.2f} | {estoque:<10}")

        print("-" * 60)
        print(f"Total de produtos: {len(produtos)}\n")
    else:
        cursor.execute("SELECT nome, preco_venda, entrada, saida FROM produtos")
        produtos = cursor.fetchall()
        conn.close()

        if not produtos:
            print("⚠️ Nenhum produto cadastrado.\n")
            return

        print("\n=== LISTA DE PRODUTOS ===")
        print(f"{'Produto':<20} | {'Valor de Venda':<15} | {'Quant. Estoque':<15}")
        print("-" * 60)

        for nome, preco_venda, entrada, saida in produtos:
            estoque = entrada - saida
            print(f"{nome:<20} | R${preco_venda:<14.2f} | {estoque:<15}")

        print("-" * 60)
        print(f"Total de produtos: {len(produtos)}\n")


def excluir_produto():
    conn = get_connection()
    cursor = conn.cursor()

    listar_produtos(True)

    try:
        idp = int(input("Digite o ID do produto que deseja excluir: "))
    except ValueError:
        print("⚠️ Entrada inválida.\n")
        return

    cursor.execute("SELECT nome FROM produtos WHERE id=?", (idp,))
    row = cursor.fetchone()
    if not row:
        print("❌ Produto não encontrado.\n")
        conn.close()
        return

    nome = row[0]
    confirm = input(f"Tem certeza que deseja excluir '{nome}' e todas as vendas associadas? (s/n): ").lower()

    if confirm != 's':
        print("❎ Exclusão cancelada.\n")
        conn.close()
        return

    cursor.execute("DELETE FROM vendas WHERE produto_id=?", (idp,))
    cursor.execute("DELETE FROM produtos WHERE id=?", (idp,))
    conn.commit()
    conn.close()
    print(f"✅ Produto '{nome}' e suas vendas foram removidos com sucesso.\n")


def editar_produto():
    conn = get_connection()
    cursor = conn.cursor()

    listar_produtos(True)

    try:
        idp = int(input("Digite o ID do produto que deseja editar: "))
    except ValueError:
        print("⚠️ Entrada inválida.\n")
        return

    cursor.execute("""
        SELECT nome, entrada, saida, preco_compra, preco_venda, validade
        FROM produtos WHERE id=?
    """, (idp,))
    row = cursor.fetchone()

    if not row:
        print("❌ Produto não encontrado.\n")
        conn.close()
        return

    nome_atual, entrada, saida, preco_compra, preco_venda, validade = row

    print("\n=== Editando produto ===")
    print(f"Nome atual: {nome_atual}")
    print(f"Estoque total: {entrada}")
    print(f"Preço de compra: R${preco_compra}")
    print(f"Preço de venda: R${preco_venda}")
    print(f"Validade: {validade if validade else 'não informada'}")

    print("\nDeixe o campo em branco para manter o valor atual.\n")

    nome_novo = input(f"Novo nome [{nome_atual}]: ").strip() or nome_atual

    try:
        entrada_nova = input(f"Nova quantidade total [{entrada}]: ").strip()
        entrada_nova = float(entrada_nova) if entrada_nova else entrada
    except ValueError:
        print("⚠️ Valor inválido para quantidade.\n")
        conn.close()
        return

    try:
        preco_compra_novo = input(f"Novo preço de compra [{preco_compra}]: ").strip()
        preco_compra_novo = float(preco_compra_novo) if preco_compra_novo else preco_compra
    except ValueError:
        print("⚠️ Valor inválido para preço de compra.\n")
        conn.close()
        return

    try:
        preco_venda_novo = input(f"Novo preço de venda [{preco_venda}]: ").strip()
        preco_venda_novo = float(preco_venda_novo) if preco_venda_novo else preco_venda
    except ValueError:
        print("⚠️ Valor inválido para preço de venda.\n")
        conn.close()
        return

    validade_nova = input(f"Nova validade (AAAA-MM-DD) [{validade or 'vazio'}]: ").strip() or validade

    cursor.execute("""
        UPDATE produtos
        SET nome=?, entrada=?, preco_compra=?, preco_venda=?, validade=?
        WHERE id=?
    """, (nome_novo, entrada_nova, preco_compra_novo, preco_venda_novo, validade_nova, idp))

    conn.commit()
    conn.close()
    print(f"✅ Produto '{nome_novo}' atualizado com sucesso!\n")


# =============================
#  FUNÇÕES USADAS PELA API
# =============================

def listar_produtos_api():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, preco_compra, preco_venda, validade FROM produtos")
    produtos = [
        {
            "id": r[0],
            "nome": r[1],
            "preco_compra": r[2],
            "preco_venda": r[3],
            "validade": r[4]
        }
        for r in cursor.fetchall()
    ]
    conn.close()
    return produtos


def cadastrar_produto_api(data: dict):
    nome = data.get("nome")
    preco_compra = data.get("preco_compra", 0.0)
    preco_venda = data.get("preco_venda", 0.0)
    validade = data.get("validade")

    if not nome:
        return {"erro": "Nome obrigatório"}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, preco_compra, preco_venda, validade)
        VALUES (?, ?, ?, ?)
    """, (nome, preco_compra, preco_venda, validade))
    conn.commit()
    conn.close()

    return {"mensagem": f"✅ Produto '{nome}' cadastrado com sucesso!"}