import streamlit as st
import yfinance as yf
import math
import plotly.graph_objects as go

# Configuração da página para Mobile
st.set_page_config(page_title="Silent Sniper Pro", page_icon="🎯", layout="centered")

# Estilização CSS para o modo escuro e botões profissionais
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button { 
        width: 100%; 
        background-color: #2e7d32; 
        color: white; 
        font-weight: bold;
        height: 3.5em;
        border-radius: 8px; 
        border: none;
        font-size: 18px;
    }
    div.stButton > button:hover { background-color: #1b5e20; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #58a6ff;'>SILENT SNIPER PRO</h1>", unsafe_allow_html=True)

# Dicionário de Apelidos
APELIDOS = {
    "PETROBRAS": "PETR4", "VALE": "VALE3", "BANCO DO BRASIL": "BBAS3",
    "BRADESCO": "BBDC4", "ITAU": "ITUB4", "ITAÚ": "ITUB4",
    "SABESP": "SBSP3", "SANEPAR": "SAPR4", "MAGALU": "MGLU3",
    "AMBEV": "ABEV3", "WEG": "WEGE3", "B3": "B3SA3",
    "EMBRAER": "EMBR3", "GERDAU": "GGBR4", "ELETROBRAS": "ELET3"
}

entrada = st.text_input("", placeholder="DIGITE O ATIVO").upper().strip()
botao_escanear = st.button("🎯 ESCANEAR ATIVO")

if botao_escanear or (entrada and not botao_escanear):
    if entrada:
        ticker = APELIDOS.get(entrada, entrada)
        t_full = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker
        
        with st.spinner(f'Sniper analisando {ticker}...'):
            try:
                acao = yf.Ticker(t_full)
                hist = acao.history(period="2mo")
                
                if not hist.empty:
                    info = acao.info
                    preco_atual = hist['Close'].iloc[-1]
                    vpa = info.get('bookValue', 0) or 0
                    lpa = info.get('trailingEps', 0