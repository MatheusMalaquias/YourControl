import sys, os
sys.path.append(os.path.dirname(__file__))

from App.Products import (
    cadastrar_produto,
    registrar_compra,
    registrar_venda,
    listar_produtos
)
from App.Simulator import simulador_interativo

def menu():
    while True:
        print("\n=== YourControl ===")
        print("1) Cadastrar produto")
        print("2) Registrar compra")
        print("3) Registrar venda")
        print("4) Listar produtos")
        print("5) Simulador financeiro")
        print("0) Sair")

        opt = input("Escolha: ").strip()

        if opt == "1":
            cadastrar_produto()
        elif opt == "2":
            registrar_compra()
        elif opt == "3":
            registrar_venda()
        elif opt == "4":
            listar_produtos()
        elif opt == "5":
            simulador_interativo()
        elif opt == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()