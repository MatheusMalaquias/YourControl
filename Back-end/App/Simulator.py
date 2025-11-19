from App.Database import load_db, load_meta, save_meta


def calcular_lucro_total(produtos):
    lucro = 0
    for p in produtos:
        lucro += p["vendas"] * (p["preco_venda"] - p["preco_compra"])
    return lucro


def simulador_interativo():
    produtos = load_db()
    if not produtos:
        print("Cadastre produtos primeiro!\n")
        return

    while True:
        print("\n=== Simulador Financeiro ===")
        print("A) Definir meta de lucro total (R$)")
        print("B) Aumentar lucro em uma porcentagem (%)")
        print("C) Sugestão automática de preços por produto")
        print("D) Meta personalizada (%)")
        print("0) Voltar")

        op = input("Escolha: ").upper().strip()

        if op == "A":
            meta = float(input("Meta de lucro desejada (R$): "))
            analisar_meta_valor(meta)

        elif op == "B":
            pct = float(input("Aumentar lucro em quantos %?: "))
            analisar_meta_percentual(pct)

        elif op == "C":
            sugestao_automatica_precos()

        elif op == "D":
            pct = float(input("Meta personalizada (%): "))
            salvar_meta_percentual(pct)
            analisar_meta_percentual(pct)

        elif op == "0":
            break

        else:
            print("Opção inválida!\n")


def salvar_meta_percentual(pct):
    meta = load_meta()
    meta["meta_percentual"] = pct
    save_meta(meta)


def analisar_meta_valor(meta_desejada):
    produtos = load_db()
    lucro_atual = calcular_lucro_total(produtos)

    print(f"\nLucro atual: R$ {lucro_atual:.2f}")
    print(f"Meta desejada: R$ {meta_desejada:.2f}")

    if lucro_atual >= meta_desejada:
        print("Meta já atingida!\n")
    else:
        restante = meta_desejada - lucro_atual
        print(f"Falta R$ {restante:.2f} para atingir a meta.\n")


def analisar_meta_percentual(pct):
    produtos = load_db()
    lucro_atual = calcular_lucro_total(produtos)

    meta = lucro_atual * (1 + pct / 100)

    print(f"\nLucro atual: R$ {lucro_atual:.2f}")
    print(f"Meta desejada (+{pct}%): R$ {meta:.2f}")
    print(f"Necessário aumentar lucro em R$ {meta - lucro_atual:.2f}\n")


def sugestao_automatica_precos():
    produtos = load_db()

    print("\n=== Sugestão automática ===")
    for p in produtos:
        custo = p["preco_compra"]
        novo_preco = custo * 1.30  # 30% acima do custo
        print(f"{p['nome']}: preço atual R${p['preco_venda']} → sugerido R${novo_preco:.2f}")

    print()