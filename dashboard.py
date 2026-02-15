import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Sentinela AI - Dashboard", layout="wide")


API_URL = "https://sentinela-api-lt0u.onrender.com" 

# --- TÍTULO E SIDEBAR ---
st.title("🛡️ Sentinela AI - Monitoramento de Ameaças")
st.markdown("### Inteligência Artificial para Detecção de Phishing e Fraudes")

# Sidebar para Status
with st.sidebar:
    st.header("Status do Sistema")
    if st.button("Testar Conexão com API"):
        try:
            response = requests.get(f"{API_URL}/")
            if response.status_code == 200:
                st.success("API Online! 🟢")
            else:
                st.error(f"Erro: {response.status_code}")
        except:
            st.error("API Offline ou Dormindo (Render Free Tier) 🔴")
    
    st.info("Nota: Se a API estiver no plano gratuito, a primeira análise pode levar 50s para 'acordar' o servidor.")

# --- ÁREA DE ANÁLISE ---
st.divider()
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Nova Análise")
    texto_input = st.text_area("Cole o texto suspeito aqui (E-mail, SMS, Link):", height=150)
    
    if st.button("Analisar Ameaça", type="primary"):
        if not texto_input:
            st.warning("Digite algum texto para analisar.")
        else:
            with st.spinner("A IA está analisando... (pode demorar se o servidor estiver dormindo)"):
                try:
                    payload = {"texto": texto_input}
                    response = requests.post(f"{API_URL}/analisar", json=payload)
                    
                    if response.status_code == 200:
                        resultado = response.json()
                        
                        # Exibe o resultado com cores dinâmicas
                        risco = resultado['nivel_risco']
                        if risco > 70:
                            st.error(f"🚨 ALTO RISCO DETECTADO: {risco}%")
                        elif risco > 30:
                            st.warning(f"⚠️ RISCO MÉDIO: {risco}%")
                        else:
                            st.success(f"✅ SEGURO: {risco}%")
                            
                        st.write(f"**Classificação:** {resultado['classificacao']}")
                        st.write(f"**Justificativa:** {resultado['justificativa']}")
                        
                        if resultado['entidades']:
                            st.write("**Entidades Suspeitas:**")
                            st.json(resultado['entidades'])
                            
                    else:
                        st.error("Erro na análise da API.")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")

# --- ÁREA DE DADOS (HISTÓRICO) ---
with col2:
    st.subheader("📊 Estatísticas")
    # Busca o histórico para montar gráficos
    try:
        response_hist = requests.get(f"{API_URL}/historico")
        if response_hist.status_code == 200:
            dados = response_hist.json()
            if dados:
                df = pd.DataFrame(dados)
                
                # Gráfico 1: Classificações
                contagem = df['classificacao'].value_counts().reset_index()
                contagem.columns = ['Classificação', 'Total']
                fig = px.pie(contagem, values='Total', names='Classificação', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
                
                # Métrica rápida
                st.metric("Total de Ameaças Analisadas", len(df))
            else:
                st.info("Nenhum dado no histórico ainda.")
    except:
        st.write("Conectando ao banco de dados...")

# --- TABELA DE LOGS ---
st.divider()
st.subheader("📜 Logs Recentes do Banco de Dados")
if 'df' in locals() and not df.empty:
    st.dataframe(df[['id', 'data_analise', 'classificacao', 'nivel_risco', 'texto_original']], use_container_width=True)