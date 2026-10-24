import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(
    page_title="Análise de Lotes e Mistura de Rações - UFC",
    page_icon="🐟",
    layout="wide"
)

st.title("🐟 Análise de Lotes de Peixes e Mistura de Rações")
st.markdown("Ferramenta para tomada de decisão alimentar baseada em amostragem por lotes (Estação de Aquicultura - UFC).")

# 1. UPLOAD DO ARQUIVO
st.sidebar.header("1. Upload de Dados")
arquivo_carregado = st.sidebar.file_uploader("Envie a planilha (.xlsx ou .csv)", type=["xlsx", "csv"])

if arquivo_carregado is not None:
    try:
        if arquivo_carregado.name.endswith(".csv"):
            df_bruto = pd.read_csv(arquivo_carregado)
        else:
            df_bruto = pd.read_excel(arquivo_carregado)
            
        st.success(f"Arquivo **{arquivo_carregado.name}** carregado com sucesso!")
        
        # 2. SELEÇÃO DE COLUNAS
        st.sidebar.header("2. Mapeamento de Colunas")
        colunas = list(df_bruto.columns)
        
        col_tanque_def = next((c for c in colunas if any(k in c.lower() for k in ['tanq', 'lote', 'setor'])), colunas[0])
        col_qtd_def = next((c for c in colunas if any(k in c.lower() for k in ['qtd', 'quant', 'num'])), colunas[1] if len(colunas) > 1 else colunas[0])
        col_peso_def = next((c for c in colunas if any(k in c.lower() for k in ['peso', 'biomassa'])), colunas[2] if len(colunas) > 2 else colunas[0])
        
        col_tanque = st.sidebar.selectbox("Coluna Tanque/Setor:", colunas, index=colunas.index(col_tanque_def))
        col_qtd = st.sidebar.selectbox("Coluna Quantidade:", colunas, index=colunas.index(col_qtd_def))
        col_peso = st.sidebar.selectbox("Coluna Peso Total (g):", colunas, index=colunas.index(col_peso_def))
        
        # Treatment and Clean Up
        df_temp = df_bruto.copy()
        df_temp[col_qtd] = pd.to_numeric(df_temp[col_qtd], errors='coerce')
        df_temp[col_peso] = pd.to_numeric(df_temp[col_peso], errors='coerce')
        
        mascara_valida = (
            df_temp[col_tanque].notnull() &
            df_temp[col_qtd].notnull() & 
            df_temp[col_peso].notnull() & 
            (df_temp[col_qtd] > 0) & 
            (df_temp[col_peso] > 0)
        )
        
        df_validado = df_temp[mascara_valida].copy()
        df_validado[col_qtd] = df_validado[col_qtd].astype(int)
        df_validado['peso_medio_g'] = df_validado[col_peso] / df_validado[col_qtd]
        
        tanques_disponiveis = sorted(list(df_validado[col_tanque].astype(str).unique()))
        
        # 3. SELEÇÃO DE PARÂMETROS
        st.sidebar.header("3. Parâmetros de Análise")
        tanque_selecionado = st.sidebar.selectbox("Selecionar Tanque para Análise:", tanques_disponiveis)
        
        limite_peq = st.sidebar.number_input("Peso máx. Pequenos (g):", value=12.0, step=0.5)
        limite_med = st.sidebar.number_input("Peso máx. Intermediários (g):", value=25.0, step=0.5)
        
        gran_peq = st.sidebar.text_input("Granulometria Pequenos:", "2.0 mm")
        gran_med = st.sidebar.text_input("Granulometria Intermediários:", "3.0 mm")
        gran_grande = st.sidebar.text_input("Granulometria Grandes:", "3.0 mm")
        
        racao_total_g = st.sidebar.number_input("Meta Alimentar Diária Total (g):", value=1000.0, step=50.0)
        num_tratos = st.sidebar.number_input("Quantidade de Tratos/Dia:", value=4, min_value=1, step=1)
        
        # EXECUÇÃO DOS CÁLCULOS
        if st.sidebar.button("Calcular Mistura de Rações"):
            df_tanque = df_validado[df_validado[col_tanque].astype(str) == str(tanque_selecionado)].copy()
            
            def classificar(pm):
                if pm <= limite_peq:
                    return 'Pequenos'
                elif pm <= limite_med:
                    return 'Intermediários'
                else:
                    return 'Grandes'
                    
            df_tanque['grupo'] = df_tanque['peso_medio_g'].apply(classificar)
            
            resumo = df_tanque.groupby('grupo', observed=False).agg(
                qtd_lotes=('peso_medio_g', 'count'),
                qtd_peixes=(col_qtd, 'sum'),
                biomassa_g=(col_peso, 'sum')
            ).reindex(['Pequenos', 'Intermediários', 'Grandes']).fillna(0)
            
            total_peixes = resumo['qtd_peixes'].sum()
            resumo['pct_peixes'] = (resumo['qtd_peixes'] / total_peixes * 100) if total_peixes > 0 else 0
            
            pct_pequenos = resumo.loc['Pequenos', 'pct_peixes']
            racao_menor_g = racao_total_g * (pct_pequenos / 100.0)
            racao_principal_g = racao_total_g - racao_menor_g
            
            # EXIBIÇÃO DOS RESULTADOS
            st.subheader(f"📊 Relatório de Análise — Tanque/Setor: {tanque_selecionado}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("População Estimada", f"{total_peixes:,.0f} peixes")
            col2.metric("Biomassa Total", f"{df_tanque[col_peso].sum()/1000:,.2f} kg")
            col3.metric("Ração para Menores", f"{pct_pequenos:.1f}% do total")
            
            st.markdown("### Distribuição da População por Faixa de Tamanho")
            df_exibe = resumo.copy()
            df_exibe['Granulometria'] = [gran_peq, gran_med, gran_grande]
            df_exibe.columns = ['Nº Lotes', 'Qtd Peixes', 'Biomassa (g)', 'Proporção (%)', 'Granulometria']
            st.dataframe(df_exibe.style.format({'Qtd Peixes': '{:,.0f}', 'Biomassa (g)': '{:,.2f}', 'Proporção (%)': '{:.2f}%'}), use_container_width=True)
            
            st.markdown("### 🥣 Plano Diário de Mistura de Ração")
            if gran_peq == gran_med == gran_grande:
                st.info("Todos os grupos utilizam a mesma granulometria. Não é necessário realizar mistura.")
            else:
                st.write(f"• **Ração de Partículas Menores ({gran_peq}):** {racao_menor_g:,.2f} g/dia ({racao_menor_g/num_tratos:,.2f} g/trato)")
                st.write(f"• **Ração Principal ({gran_med}):** {racao_principal_g:,.2f} g/dia ({racao_principal_g/num_tratos:,.2f} g/trato)")
            
            # GRÁFICOS
            st.markdown("### 📈 Visualização Gráfica")
            fig, ax = plt.subplots(1, 2, figsize=(12, 4))
            
            ax[0].pie(resumo['qtd_peixes'], labels=resumo.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'], startangle=140)
            ax[0].set_title("Distribuição da População")
            
            ax[1].bar(["Ração Menor", "Ração Principal"], [racao_menor_g, racao_principal_g], color=['#ff9999', '#66b3ff'])
            ax[1].set_ylabel("Gramas (g)")
            ax[1].set_title("Composição Diária da Ração")
            
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Aguardando upload da planilha no painel à esquerda.")