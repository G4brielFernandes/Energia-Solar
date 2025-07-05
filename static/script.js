let ultimoResultado = null;
let inversores = [];

// 1️⃣ Carrega inversores
fetch("/inversores")
  .then(res => res.json())
  .then(data => inversores = data);

// 2️⃣ Carrega cidades para Awesomplete
fetch("/cidades")
  .then(res => res.json())
  .then(cidades => {
    new Awesomplete(document.getElementById("cidade"), {
      list: cidades
    });
  });

// 3️⃣ Botão Calcular
document.getElementById("calcular").onclick = () => {
  const cidade = document.getElementById("cidade").value.trim();
  const kwh = document.getElementById("kwh").value.trim();
  const potencia = document.getElementById("potencia").value;

  if (!cidade || !kwh) {
    alert("Preencha todos os campos!");
    return;
  }

  fetch("/calcular", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cidade, kwh, potencia })
  })
    .then(res => res.json())
    .then(r => {
      ultimoResultado = r;

      // Mostra resultado ORIGINAL formatado COMPLETO
      document.getElementById("original").textContent =
`🔆 Potência necessária: ${r.kwp} kWp
🔆 Placas: ${r.placas}
💰 Economia em 25 anos: R$ ${r.economia_25anos}
⚡ Inversor: ${r.modelo_inversor} (${r.max_inversor} kWp)
⚡ Geração máx: ${r.kwh_maximo} kWh
🔩 Máx placas: ${r.placas_maximo}
📐 Área: ${r.area} m²
🔌 Conectores: ${r.conector}`;

      // Torna o resultado visível com animação
      document.querySelector("#original").parentElement.classList.add("visible");

      // Monta lista de inversores
      const select = document.getElementById("inversor");
      select.innerHTML = "";
      inversores.forEach(inv => {
        const opt = document.createElement("option");
        opt.value = JSON.stringify(inv);
        opt.textContent = `${inv.modelo} (${inv.kwp} kWp)`;
        select.appendChild(opt);
      });

      document.getElementById("inversor-box").classList.remove("hidden");
    });
};



// 4️⃣ Troca inversor
document.getElementById("inversor").onchange = () => {
  if (!ultimoResultado) return;

  const novo = JSON.parse(document.getElementById("inversor").value);

  fetch("/personalizar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      resultado_anterior: ultimoResultado,
      modelo: novo.modelo,
      max_kwp: novo.kwp
    })
  })
    .then(res => res.json())
    .then(r => {
      document.getElementById("personalizado").textContent =
`⚡ Inversor: ${r.modelo_inversor} (${r.max_inversor} kWp)
⚡ Geração máx: ${r.kwh_maximo} kWh
🔩 Máx placas: ${r.placas_maximo}`;

      document.querySelector("#personalizado").parentElement.classList.add("visible");
    });
};

document.getElementById("resetar").onclick = () => {
  document.getElementById("cidade").value = "";
  document.getElementById("kwh").value = "";
  document.getElementById("potencia").value = "700";
  document.getElementById("original").textContent = "";
  document.getElementById("personalizado").textContent = "";
  document.querySelector("#original").parentElement.classList.remove("visible");
  document.querySelector("#personalizado").parentElement.classList.remove("visible");
  document.getElementById("inversor-box").classList.add("hidden");
};