from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from Routes import Products
from App.Analysis import gerar_relatorio

app = FastAPI(title="YourControl API")

# === Permitir acesso do front-end (CORS) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou substitua por ["http://localhost:5173"] se usar Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ROTAS ===

@app.get("/produtos")
def listar():
    """Retorna lista de produtos para o front-end."""
    return Products.listar_produtos_api()


@app.post("/produtos")
def cadastrar(produto: dict = Body(...)):
    """Cadastra um novo produto via JSON."""
    return Products.cadastrar_produto_api(produto)


@app.get("/relatorio")
def relatorio():
    """Gera relatório geral de vendas e produtos."""
    return gerar_relatorio(exportar=False)