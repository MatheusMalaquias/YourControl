import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from App.Analysis import (
    gerar_relatorio,
    enviar_relatorio_whatsapp,
    sugestao_precos_para_meta,
    simulador_financeiro
)
from Routes.Products import (
    cadastrar_produto,
    registrar_compra,
    registrar_venda,
    listar_produtos,
    excluir_produto,
    editar_produto
)
from App.Config import definir_meta_total, definir_whatsapp

def menu():
    while True:
        print("=== YourControl ===")
        print("1) Cadastrar produto")
        print("2) Registrar compra")
        print("3) Registrar venda")
        print("4) Definir meta total de lucro")
        print("5) Listar produtos")
        print("6) Ver relatório")
        print("7) Exportar relatório CSV")
        print("8) Definir número do WhatsApp")
        print("9) Enviar relatório via WhatsApp")
        print("10) Excluir produto")
        print("11) Editar produto")
        print("12) Sugerir novos preços para atingir a meta")
        print("13) Simulador financeiro")
        print("0) Sair")

        opc = input("Escolha uma opção: ").strip()

        if opc == '1': cadastrar_produto()
        elif opc == '2': registrar_compra()
        elif opc == '3': registrar_venda()
        elif opc == '4': definir_meta_total()
        elif opc == '5': listar_produtos()
        elif opc == '6': gerar_relatorio()
        elif opc == '7': gerar_relatorio(exportar=True)
        elif opc == '8': definir_whatsapp()
        elif opc == '9': enviar_relatorio_whatsapp()
        elif opc == '10': excluir_produto()
        elif opc == '11': editar_produto()
        elif opc == '12': sugestao_precos_para_meta()
        elif opc == '13': simulador_financeiro()
        elif opc == '0':
            print("Saindo...\n")
            break
        else:
            print("Opção inválida.\n")

if __name__ == "__main__":
    menu()