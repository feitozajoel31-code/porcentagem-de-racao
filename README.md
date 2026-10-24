# porcentagem-de-racao
programa destinado a calcular a porcentagem de ração para tanques de aquicultura
# 🐟 Análise de Lotes de Peixes e Calculadora de Mistura de Rações

Este projeto é uma ferramenta desenvolvida em Python/Streamlit para auxiliar nas decisões de manejo alimentar e transição de rações na **Estação de Aquicultura da Universidade Federal do Ceará (UFC)**.

O objetivo do programa é analisar planilhas de biometria com dados de amostragem por lotes (ou indivíduos), identificar os grupos de tamanho presentes em cada tanque e calcular a proporção exata de ração de granulometria menor que deve ser incorporada à ração principal.

---

## 🚀 Funcionalidades

- **Upload Flexível:** Aceita arquivos nos formatos `.xlsx` (Excel) e `.csv`.
- **Mapeamento Dinâmico de Colunas:** Permite ao usuário selecionar manualmente quais colunas representam o Tanque, a Quantidade de Peixes e o Peso Total.
- **Validação Automática:** Filtra linhas com dados nulos, zerados ou inválidos, apresentando um relatório de consistência.
- **Suporte Multi-Tanques:** Permite escolher qual tanque/setor analisar individualmente.
- **Classificação por Faixas de Peso:** Categorização configurável em peixes *Pequenos*, *Intermediários* e *Grandes*.
- **Cálculo da Mistura de Rações:** Determina a porcentagem e a quantidade diária em gramas (e por trato) para a ração de partículas menores e para a ração principal.
- **Visualização Gráfica:** Gera gráficos interativos da distribuição da população e da composição da dieta.

---

## 📊 Estrutura Recomendada da Planilha

O programa aceita qualquer nome de coluna, desde que a planilha contenha no mínimo:

1. **Identificador do Tanque/Setor** (ex: `Tanque`, `Setor`, `Lote`).
2. **Quantidade de Peixes no Lote** (ex: `QTD`, `Quantidade`, `Num_Peixes`).
3. **Peso Total do Lote em Gramas** (ex: `PESO`, `Peso_g`, `Biomassa`).

> **Nota:** Se a sua planilha contiver pesagens individuais, basta registrar a quantidade (`QTD`) como `1` em cada linha.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit** (Interface Web)
- **Pandas** (Processamento e análise de dados)
- **Matplotlib** (Visualização de dados)
- **OpenPyXL** (Leitura de arquivos Excel)

---

## 📌 Limitações e Observações Técnicas

1. **Estimativa por Peso Médio:** Na rotina em que os alevinos são pesados em lotes (ex: 20 a 40 peixes), o peso individual de cada peixe é representado pelo peso médio do lote ($\text{Peso Total} / \text{Quantidade}$). O programa respeita essa limitação sem simular variações individuais não registradas.
2. **Regra Operacional da Mistura:** A substituição da ração principal pela ração de granulometria menor na mesma proporção do percentual de peixes pequenos constitui uma regra operacional inicial, que deve ser validada e ajustada tecnicamente conforme a orientação da Profa. Suzete.
