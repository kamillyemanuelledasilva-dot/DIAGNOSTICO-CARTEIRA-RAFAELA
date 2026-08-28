import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da página
st.set_page_config(page_title="Diagnóstico de Carteira", page_icon="📊", layout="wide")

st.title("📊 Diagnóstico de Carteira - Semanal")
st.markdown("Acompanhamento das prospecções e renovações da carteira, destacando casos em análise e pendências.")
st.markdown("---")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    try:
        # Carrega o arquivo usando ponto-e-vírgula como separador
        df = pd.read_csv("dados_semanais.csv", encoding="utf-8", sep=";")
        return df
    except FileNotFoundError:
        st.error("⚠️ Arquivo 'dados_semanais.csv' não encontrado.")
        return pd.DataFrame()

df = carregar_dados()

if not df.empty:
    # ----------------------------------------------------
    # CÁLCULO DOS INDICADORES
    # ----------------------------------------------------
    em_analise = len(df[df['Status'] == 'Em Análise de Crédito'])
    prosp_pendentes = len(df[(df['Fase'] == 'Prospecção') & (df['Status'] == 'Com Pendências')])
    renov_pendentes = len(df[((df['Fase'] == 'Renovação') | (df['Fase'] == 'Risco Sacado')) & (df['Status'] == 'Com Pendências')])
    total_casos = len(df)

    # ----------------------------------------------------
    # EXIBIÇÃO DOS KPIs (CAIXAS DE RESUMO)
    # ----------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"🔵 **Em Análise de Crédito:**\n\n# {em_analise} casos")
    
    with col2:
        st.warning(f"🟡 **Prospecções c/ Pendências:**\n\n# {prosp_pendentes} casos")
        
    with col3:
        st.error(f"🔴 **Renovações c/ Pendências:**\n\n# {renov_pendentes} casos")

    with col4:
        st.success(f"📋 **Total em Acompanhamento:**\n\n# {total_casos} casos")
        
    st.markdown("---")
    
    # ----------------------------------------------------
    # GRÁFICOS
    # ----------------------------------------------------
    st.subheader("Visão Geral do Status")
    
    # Criar uma coluna combinada para o gráfico ficar igual ao e-mail
    def definir_categoria(row):
        if row['Status'] == 'Em Análise de Crédito':
            return '🔵 Em análise'
        elif row['Fase'] == 'Prospecção' and row['Status'] == 'Com Pendências':
            return '🟡 Prospecções pendentes'
        else:
            return '🔴 Renovações pendentes'

    df['Categoria_Grafico'] = df.apply(definir_categoria, axis=1)
    
    col_graf1, col_graf2 = st.columns([1, 2])
    
    with col_graf1:
        fig1 = px.pie(
            df, 
            names="Categoria_Grafico", 
            hole=0.4,
            color="Categoria_Grafico",
            color_discrete_map={
                "🔵 Em análise": "#3b82f6",
                "🟡 Prospecções pendentes": "#eab308",
                "🔴 Renovações pendentes": "#ef4444"
            }
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col_graf2:
        st.markdown("""
        **📌 Legenda e Ações:**
        * **🔵 Em análise:** documentação em andamento / apresentação em elaboração ou em análise pelo Comitê. (Acompanhar evolução)
        * **🟡 Prospecção:** cadastro iniciado, porém com pendências documentais que impedem o avanço. (Atuar na regularização)
        * **🔴 Renovação:** documentação pendente para continuidade da análise; avaliar standby nos casos sem previsão de envio.
        """)
        
        st.warning("⚠️ **Ponto de Atenção:** Recomendamos priorizar os processos com pendências documentais para evitar que permaneçam parados e avaliarmos quais renovações devem ser colocadas em standby.")

    st.markdown("---")
    
    # ----------------------------------------------------
    # TABELAS DETALHADAS
    # ----------------------------------------------------
    st.subheader("📌 1. EMPRESAS EM ANÁLISE DE CRÉDITO")
    df_analise = df[df['Status'] == 'Em Análise de Crédito']
    st.dataframe(df_analise[['Cliente', 'Detalhes', 'Ação Necessária']], use_container_width=True, hide_index=True)

    st.subheader("📌 2. PROSPECÇÕES COM PENDÊNCIAS")
    df_prosp = df[(df['Fase'] == 'Prospecção') & (df['Status'] == 'Com Pendências')]
    st.dataframe(df_prosp[['Cliente', 'Detalhes', 'Ação Necessária']], use_container_width=True, hide_index=True)

    st.subheader("📌 3. RENOVAÇÕES COM PENDÊNCIAS")
    st.caption("Gentileza verificar a possibilidade de colocarmos em standby nos casos sem previsão de regularização.")
    df_renov = df[((df['Fase'] == 'Renovação') | (df['Fase'] == 'Risco Sacado')) & (df['Status'] == 'Com Pendências')]
    st.dataframe(df_renov[['Cliente', 'Fase', 'Detalhes', 'Ação Necessária']], use_container_width=True, hide_index=True)

else:
    st.info("O painel está aguardando os dados para gerar os gráficos.")
