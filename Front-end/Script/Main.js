const API_BASE = "http://127.0.0.1:8000"; // Ajuste conforme o backend

// === Alternar telas ===
function mostrarTela(nome) {
  document.querySelectorAll(".tela").forEach(sec => sec.classList.remove("ativa"));
  document.getElementById(`tela-${nome}`).classList.add("ativa");
}

// === Carregar produtos ===
async function carregarProdutos() {
  const lista = document.getElementById("listaProdutos");
  lista.innerHTML = "<li>Carregando...</li>";

  try {
    const res = await fetch(`${API_BASE}/produtos`);
    const produtos = await res.json();

    lista.innerHTML = "";
    if (produtos.length === 0) {
      lista.innerHTML = "<li>Nenhum produto cadastrado.</li>";
      return;
    }

    produtos.forEach(p => {
      const li = document.createElement("li");
      li.textContent = `${p.nome} — Compra: R$${p.preco_compra} | Venda: R$${p.preco_venda}`;
      lista.appendChild(li);
    });
  } catch (e) {
    lista.innerHTML = `<li>Erro ao carregar: ${e.message}</li>`;
  }
}

// === Cadastro de novo produto ===
document.getElementById("formCadastro").addEventListener("submit", async e => {
  e.preventDefault();
  const nome = document.getElementById("nome").value;
  const preco_compra = parseFloat(document.getElementById("preco_compra").value);
  const preco_venda = parseFloat(document.getElementById("preco_venda").value);
  const validade = document.getElementById("validade").value || null;

  try {
    const res = await fetch(`${API_BASE}/produtos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, preco_compra, preco_venda, validade })
    });

    if (res.ok) {
      alert("✅ Produto cadastrado com sucesso!");
      e.target.reset();
      mostrarTela("produtos");
      carregarProdutos();
    } else {
      alert("❌ Erro ao cadastrar produto!");
    }
  } catch (e) {
    alert("Erro de conexão com o servidor.");
  }
});

// === Relatório simples ===
document.getElementById("btnRelatorio").addEventListener("click", async () => {
  const saida = document.getElementById("saidaRelatorio");
  saida.textContent = "Gerando relatório...";

  try {
    const res = await fetch(`${API_BASE}/relatorio`);
    const data = await res.json();
    saida.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    saida.textContent = `Erro: ${e.message}`;
  }
});

// === Inicialização ===
document.getElementById("btnCarregar").addEventListener("click", carregarProdutos);
carregarProdutos();