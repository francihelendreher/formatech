import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# FORMATECH - ANÁLISE DE DADOS
# NumPy + Pandas + Matplotlib
# ==========================================


def brl(valor):
    """Formata um número no padrão brasileiro: 1234.5 -> 1.234,50"""
    texto = f"{valor:,.2f}"                     # 1,234.50 (padrão americano)
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


# 1. CARREGAMENTO DOS DADOS

df = pd.read_csv(
    "vendas_brutas_formatech.csv",
    sep=";",
    decimal=",",
    thousands=".",
    encoding="utf-8-sig"
)

print("\n========== FORMATECH ==========")
print("ANÁLISE DE DADOS")
print("================================")

# 2. LIMPEZA E CÁLCULOS ESTATÍSTICOS

lucros = pd.to_numeric(
    df["lucro_venda"],
    errors="coerce"
).dropna().to_numpy()

if len(lucros) == 0:
    raise ValueError("Nenhum valor numérico válido em 'lucro_venda'.")

media = np.mean(lucros)
mediana = np.median(lucros)

# ddof=1: estamos trabalhando com uma amostra de vendas
desvio = np.std(lucros, ddof=1)
variancia = np.var(lucros, ddof=1)

q1, q2, q3 = np.percentile(lucros, [25, 50, 75])
iqr = q3 - q1

limite_inf = q1 - 1.5 * iqr
limite_sup = q3 + 1.5 * iqr

outliers = lucros[(lucros < limite_inf) | (lucros > limite_sup)]

print("\n--- ESTATÍSTICA ---")
print(f"Média: R$ {brl(media)}")
print(f"Mediana: R$ {brl(mediana)}")
print(f"Desvio padrão: R$ {brl(desvio)}")
print(f"Variância: {brl(variancia)}")

print("\n--- QUARTIS ---")
print(f"Q1: R$ {brl(q1)}")
print(f"Q2: R$ {brl(q2)}")
print(f"Q3: R$ {brl(q3)}")
print(f"IQR: R$ {brl(iqr)}")

print("\n--- VALORES EXTREMOS ---")
print(f"Limite inferior: R$ {brl(limite_inf)}")
print(f"Limite superior: R$ {brl(limite_sup)}")
print(f"Quantidade de outliers: {len(outliers)}")
if len(outliers) > 0:
    print("Outliers:", ", ".join(f"R$ {brl(v)}" for v in outliers))

print("\n--- EXTREMOS GERAIS ---")
print(f"Menor lucro: R$ {brl(np.min(lucros))}")
print(f"Maior lucro: R$ {brl(np.max(lucros))}")
print(f"Amplitude: R$ {brl(np.ptp(lucros))}")

# 3. INTERPOLAÇÃO QUADRÁTICA

# ATENÇÃO: valores ilustrativos, não são os dados reais.
# Substituir pelos lucros mensais reais quando estiverem disponíveis.

meses = np.array([1, 2, 3])

lucros_mensais = np.array([
    12000,
    18500,
    26000
])

# Com 3 pontos, a parábola passa exatamente por todos eles (interpolação)
coef = np.polyfit(meses, lucros_mensais, 2)
funcao = np.poly1d(coef)

estimativa = funcao(2.5)

print("\n--- INTERPOLAÇÃO QUADRÁTICA (dados ilustrativos) ---")
print("Coeficientes:", coef)
print("Função:", funcao)
print(f"Estimativa para o mês 2,5: R$ {brl(estimativa)}")

# 4. CONFIGURAÇÃO VISUAL

plt.style.use("dark_background")

fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor("#171526")

# 5. EVOLUÇÃO DOS LUCROS

axs[0, 0].plot(
    np.arange(1, len(lucros) + 1),
    lucros,
    color="#C5A7FF",
    marker="o",
    markersize=4
)
axs[0, 0].set_title("FormaTech | Evolução dos Lucros", color="#E9DDFB")
axs[0, 0].set_xlabel("Venda nº")
axs[0, 0].set_ylabel("Lucro (R$)")
axs[0, 0].grid(alpha=0.2)

# 6. DISTRIBUIÇÃO DOS LUCROS

axs[0, 1].hist(
    lucros,
    bins=10,
    color="#A78BFA",
    edgecolor="#E9DDFB",
    alpha=0.8
)
axs[0, 1].set_title("Distribuição dos Lucros", color="#E9DDFB")
axs[0, 1].set_xlabel("Lucro (R$)")
axs[0, 1].set_ylabel("Frequência")

# 7. BOXPLOT E OUTLIERS

axs[1, 0].boxplot(
    lucros,
    vert=True,
    patch_artist=True,
    boxprops=dict(facecolor="#A78BFA", color="#E9DDFB"),
    medianprops=dict(color="#FFFFFF"),
    flierprops=dict(markerfacecolor="#FF8FA3", marker="o")
)
axs[1, 0].set_title("Boxplot dos Lucros", color="#E9DDFB")
axs[1, 0].set_ylabel("Lucro (R$)")

# 8. INTERPOLAÇÃO QUADRÁTICA

x_curva = np.linspace(1, 3, 100)

axs[1, 1].scatter(
    meses,
    lucros_mensais,
    color="#E9DDFB",
    label="Valores observados (ilustrativos)"
)
axs[1, 1].plot(
    x_curva,
    funcao(x_curva),
    color="#C5A7FF",
    linestyle="--",
    label="Curva quadrática"
)
axs[1, 1].scatter(
    2.5,
    estimativa,
    color="#FF8FA3",
    label="Estimativa (mês 2,5)"
)
axs[1, 1].set_title("Interpolação Quadrática", color="#E9DDFB")
axs[1, 1].set_xlabel("Mês")
axs[1, 1].set_ylabel("Lucro (R$)")
axs[1, 1].legend()

# 9. FINALIZAÇÃO

for ax in axs.flat:
    ax.tick_params(colors="#E9DDFB")
    ax.xaxis.label.set_color("#E9DDFB")
    ax.yaxis.label.set_color("#E9DDFB")

plt.suptitle("FormaTech | Dashboard de Lucros", color="#E9DDFB", fontsize=16)
plt.tight_layout()

plt.savefig(
    "formatech_dashboard.png",
    dpi=300,
    facecolor=fig.get_facecolor()
)

plt.show()

print("\nDashboard gerado com sucesso!")
