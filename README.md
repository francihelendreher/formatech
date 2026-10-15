# Projeto de Educação Profissional - análise de vendas 
Fundamentos de manipulação e análise exploratória com Pandas. Não é um sistema financeiro nem uma apuração contábil.

Projeto fictício de portfólio para praticar criação/importação de DataFrames, inspeção, limpeza, transformação, filtros, agrupamentos, ordenação e exportação com Python e Pandas.
Aviso: a empresa e todos os registros são fictícios. Os números não representam resultados reais.

*Objetivo*

Organizar uma base de vendas de cursos técnicos, melhorar a qualidade dos dados e produzir tabelas que ajudem a explorar faturamento, custos e lucro estimado por curso, modalidade, período e status de pagamento.

Arquivos
• vendas_brutas_formatech.csv: base bruta com inconsistências intencionais para praticar limpeza.
• analise_formatech.py: script principal com o fluxo de análise.
• Os CSVs de resultados são gerados quando o script é executado.

*Como executar*

1. Tenha Python e Pandas disponíveis no ambiente.
2. Deixe analise_formatech.py e vendas_brutas_formatech.csv na mesma pasta.
3. Execute python analise_formatech.py.
O projeto usa sep=";" e codificação UTF-8 com BOM nos arquivos CSV exportados para facilitar a abertura em planilhas.

*Etapas trabalhadas*

1. Inspeção com head(), shape, dtypes e isnull().sum().
2. Verificação de IDs duplicados.
3. Padronização de textos com astype(), str.strip(), str.title() e str.lower().
4. Conversão de tipos com to_datetime() e to_numeric().
5. Tratamento explícito de valores ausentes e duplicidade de ID.
6. Criação de colunas calculadas.
7. Classificações com apply() e lambda.
8. Renomeação com rename().
9. Filtros com condições e operadores lógicos.
10. Agrupamentos com groupby() e agg().
11. Ordenação com sort_values().
12. Exportação com to_csv().
    
*Cuidados de interpretação*

• faturamento líquido = quantidade × valor unitário − desconto.
• custo total = quantidade × custo unitário.
• lucro estimado = faturamento líquido − custo total.
• Indicadores de recebimento consideram apenas vendas com status Pago. O lucro aqui é uma estimativa didática e não inclui despesas fixas, impostos ou comissões.
• No tratamento demonstrativo, desconto ausente é considerado zero; cliente ausente vira Não informado; quantidade ausente recebe 1 como regra didática. Em um projeto real, essas decisões precisariam ser validadas com a área responsável.

• A remoção de IDs duplicados mantém a primeira ocorrência. Em contexto real, seria necessário investigar o motivo da duplicidade antes de descartar registros.
