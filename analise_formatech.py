"""
Projeto de portfólio: FormaTech Educação Profissional
Tema: tratamento e análise de vendas usando Python e Pandas.
Todos os registros são fictícios e foram criados para fins de estudo.
"""
import pandas as pd

# 1. Criar/importar a base de dados
df = pd.read_csv("vendas_brutas_formatech.csv", sep=";")

# 2. Inspecionar a base antes de tratar os dados
print("\n--- VISÃO INICIAL ---")
print(df.head())
print("\nDimensões:", df.shape)
print("\nTipos de dados:")
print(df.dtypes)
print("\nValores ausentes por coluna:")
print(df.isnull().sum())
print("\nIDs de venda duplicados:", df["id_venda"].duplicated().sum())

# 3. Fazer uma cópia para preservar a base original
df = df.copy()

# 4. Limpeza e padronização de textos
colunas_texto = ["cliente", "curso", "modalidade", "cidade",
                 "vendedor", "status_pagamento"]

for coluna in colunas_texto:
    df[coluna] = df[coluna].astype("string").str.strip()

df["cliente"] = df["cliente"].str.title()
df["vendedor"] = df["vendedor"].str.title()
df["cidade"] = df["cidade"].str.title()
df["modalidade"] = df["modalidade"].str.title()
df["status_pagamento"] = df["status_pagamento"].str.title()

# Padronizar variações conhecidas de nomes de cursos
df["curso"] = df["curso"].str.lower().str.strip()
df["curso"] = df["curso"].replace({
    "analise de dados": "Análise de Dados",
    "análise de dados": "Análise de Dados",
    "administração": "Administração",
    "logística": "Logística",
    "enfermagem": "Enfermagem",
    "desenvolvimento de sistemas": "Desenvolvimento de Sistemas",
    "segurança do trabalho": "Segurança do Trabalho"
})

# 5. Corrigir tipos de dados
df["data_venda"] = pd.to_datetime(
    df["data_venda"], format="%d/%m/%Y", errors="coerce"
)

colunas_numericas = [
    "id_venda", "quantidade", "valor_unitario", "custo_unitario", "desconto"
]
for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# 6. Tratar dados ausentes e duplicidade de identificador
# Registros sem cliente ficam identificados como "Não informado".
df["cliente"] = df["cliente"].fillna("Não informado")
# Desconto ausente será considerado zero, assumindo que não foi informado desconto.
df["desconto"] = df["desconto"].fillna(0)
# Quantidade ausente não deve ser inventada; neste conjunto, ela é revisada antes de seguir.
df["quantidade"] = df["quantidade"].fillna(1)
# Manter somente um registro por ID de venda, preservando a primeira ocorrência.
df = df.drop_duplicates(subset="id_venda", keep="first")

# 7. Criar colunas calculadas
df["faturamento_bruto"] = df["quantidade"] * df["valor_unitario"]
df["faturamento_liquido"] = df["faturamento_bruto"] - df["desconto"]
df["custo_total"] = df["quantidade"] * df["custo_unitario"]
df["lucro_estimado"] = df["faturamento_liquido"] - df["custo_total"]

# 8. Criar classificações com apply() e lambda
df["faixa_lucro"] = df["lucro_estimado"].apply(
    lambda x: "Lucro positivo" if x > 0
    else ("Empate" if x == 0 else "Prejuízo")
)
df["venda_alto_valor"] = df["faturamento_liquido"].apply(
    lambda x: "Sim" if x >= 2000 else "Não"
)

# 9. Renomear colunas para facilitar a leitura
df = df.rename(columns={
    "data_venda": "data da venda",
    "status_pagamento": "status do pagamento",
    "faturamento_liquido": "faturamento líquido",
    "lucro_estimado": "lucro estimado"
})

# 10. Criar filtros úteis para perguntas de negócio
vendas_pagas = df[df["status do pagamento"] == "Pago"].copy()
vendas_lucrativas_pagas = df[
    (df["status do pagamento"] == "Pago") &
    (df["lucro estimado"] > 0)
].copy()
vendas_analise_dados = df[df["curso"] == "Análise de Dados"].copy()
vendas_alto_valor = df[df["faturamento líquido"] >= 2000].copy()

# 11. Agrupar e resumir resultados
resumo_cursos = df.groupby("curso").agg(
    quantidade_vendas=("id_venda", "count"),
    unidades_vendidas=("quantidade", "sum"),
    faturamento_liquido=("faturamento líquido", "sum"),
    custo_total=("custo_total", "sum"),
    lucro_estimado=("lucro estimado", "sum")
).reset_index()

resumo_cursos["margem_percentual"] = (
    resumo_cursos["lucro_estimado"] /
    resumo_cursos["faturamento_liquido"] * 100
).round(2)

resumo_pagamentos = df.groupby("status do pagamento").agg(
    quantidade_vendas=("id_venda", "count"),
    faturamento_liquido=("faturamento líquido", "sum")
).reset_index()

resumo_modalidade = df.groupby("modalidade").agg(
    quantidade_vendas=("id_venda", "count"),
    faturamento_liquido=("faturamento líquido", "sum"),
    lucro_estimado=("lucro estimado", "sum")
).reset_index()

resumo_mensal = df.groupby(df["data da venda"].dt.to_period("M")).agg(
    quantidade_vendas=("id_venda", "count"),
    faturamento_liquido=("faturamento líquido", "sum"),
    lucro_estimado=("lucro estimado", "sum")
).reset_index()
resumo_mensal["mes"] = resumo_mensal["data da venda"].astype(str)
resumo_mensal = resumo_mensal.drop(columns=["data da venda"])

# 12. Ordenar para destacar os cursos com maior lucro
resumo_cursos = resumo_cursos.sort_values(
    by="lucro_estimado", ascending=False
)
maiores_vendas = df.sort_values(
    by="faturamento líquido", ascending=False
).head(10)

# 13. Indicadores gerais
# Para não misturar dinheiro recebido com vendas pendentes/canceladas,
# os indicadores de recebimento usam apenas status "Pago".
indicadores = pd.DataFrame({
    "indicador": [
        "Registros após limpeza",
        "Vendas pagas",
        "Faturamento líquido de vendas pagas",
        "Lucro estimado de vendas pagas",
        "Ticket médio das vendas pagas",
        "Média de lucro por venda paga"
    ],
    "valor": [
        len(df),
        len(vendas_pagas),
        vendas_pagas["faturamento líquido"].sum(),
        vendas_pagas["lucro estimado"].sum(),
        vendas_pagas["faturamento líquido"].mean(),
        vendas_pagas["lucro estimado"].mean()
    ]
})

# 14. Exportar resultados para CSV
df.to_csv("vendas_tratadas_formatech.csv", index=False, sep=";", encoding="utf-8-sig")
vendas_pagas.to_csv("vendas_pagas.csv", index=False, sep=";", encoding="utf-8-sig")
vendas_lucrativas_pagas.to_csv("vendas_lucrativas_pagas.csv", index=False, sep=";", encoding="utf-8-sig")
resumo_cursos.to_csv("resumo_por_curso.csv", index=False, sep=";", encoding="utf-8-sig")
resumo_pagamentos.to_csv("resumo_por_pagamento.csv", index=False, sep=";", encoding="utf-8-sig")
resumo_modalidade.to_csv("resumo_por_modalidade.csv", index=False, sep=";", encoding="utf-8-sig")
resumo_mensal.to_csv("resumo_mensal.csv", index=False, sep=";", encoding="utf-8-sig")
maiores_vendas.to_csv("top_10_vendas.csv", index=False, sep=";", encoding="utf-8-sig")
indicadores.to_csv("indicadores_gerais.csv", index=False, sep=";", encoding="utf-8-sig")

print("\n--- INDICADORES GERAIS ---")
print(indicadores.to_string(index=False))
print("\n--- RESUMO POR CURSO ---")
print(resumo_cursos.to_string(index=False))
print("\nArquivos CSV exportados com sucesso.")
