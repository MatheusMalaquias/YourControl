import csv
from App.Database import load_db
from App.Config import load_meta

def gerar_relatorio(exportar=False):
    produtos = load_db()
    meta = load_meta()["meta"]

    lucro_total = 0
    for p in produtos:
        lucro_total += p["vendas"] * (p["preco_venda"] - p["preco_compra"])

    print("\n=== RELATÓRIO ===")
    print(f"Lucro total: R$ {lucro_total:.2f}")
    print(f"Meta: R$ {meta:.2f}")
    print(f"Progresso: {(lucro_total/meta*100) if meta else 0:.2f}%\n")

    if exportar:
        with open("relatorio.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Produto", "Vendas", "Lucro unitário"])
            for p in produtos:
                writer.writerow([p["nome"], p["vendas"], p["preco_venda"] - p["preco_compra"]])
        print("Relatório exportado!\n")


def sugestao_precos_para_meta():
    print("Função de sugestão em construção.\n")


def simulador_financeiro():
    print("Simulador financeiro em construção.\n")