from App.Database import load_db, save_db


def cadastrar_produto():
    nome = input("Nome do produto: ")
    preco_compra = float(input("Preço de compra: "))
    preco_venda = float(input("Preço de venda: "))
    quantidade = int(input("Quantidade inicial: "))

    produtos = load_db()

    produto = {
        "id": len(produtos) + 1,
        "nome": nome,
        "preco_compra": preco_compra,
        "preco_venda": preco_venda,
        "quantidade": quantidade,
        "vendas": 0
    }

    produtos.append(produto)
    save_db(produtos)
    print("Produto cadastrado!\n")


def registrar_compra():
    produtos = load_db()
    listar_produtos()

    pid = int(input("ID do produto: "))
    qtd = int(input("Quantidade comprada: "))

    for p in produtos:
        if p["id"] == pid:
            p["quantidade"] += qtd
            save_db(produtos)
            print("Compra registrada!\n")
            return

    print("Produto não encontrado!\n")


def registrar_venda():
    produtos = load_db()
    listar_produtos()

    pid = int(input("ID do produto: "))
    qtd = int(input("Quantidade vendida: "))

    for p in produtos:
        if p["id"] == pid:
            if qtd > p["quantidade"]:
                print("Estoque insuficiente!\n")
                return
            p["quantidade"] -= qtd
            p["vendas"] += qtd
            save_db(produtos)
            print("Venda registrada!\n")
            return

    print("Produto não encontrado!\n")


def listar_produtos():
    produtos = load_db()
    print("\n=== Produtos ===")
    for p in produtos:
        print(f"ID: {p['id']} | {p['nome']} | Estoque: {p['quantidade']} | Venda: R${p['preco_venda']}")
    print()