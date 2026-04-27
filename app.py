import streamlit as st
import yfinance as yf
import math
import pandas as pd

st.set_page_config(page_title="Silent Sniper Pro", page_icon="🎯")

st.markdown("<h1 style='text-align: center; color: #58a6ff;'>SILENT SNIPER PRO</h1>", unsafe_allow_html=True)

# Dicionário de tradução otimizado
APELIDOS = {
    "PETROBRAS": "PETR4", "VALE": "VALE3", "BANCO DO BRASIL": "BBAS3",
    "BRADESCO": "BBDC4", "ITAU": "ITUB4", "ITAÚ": "ITUB4",
    "SABESP": "SBSP3", "SANEPAR": "SAPR4", "MAGALU": "MGLU3",
    "AMBEV": "ABEV3", "WEG": "WEGE3", "B3": "B3SA3",
    "EMBRAER": "EMBR3", "GERDAU": "GGBR4", "ELETROBRAS": "ELET3",
    "COSAN": "CSAN3", "LOCALIZA": "RENT3", "CEMIG": "CMIG4",
    "TAEEA": "TAEE11", "AZUL": "AZUL4", "GOL": "GOLL4"
}

entrada_usuario = st.text_input("DIGITE O NOME OU O CÓDIGO", "").upper().strip()

if entrada_usuario:
    ticker = APELIDOS.get(entrada_usuario, entrada_usuario)
    t_full = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker
    
    with st.spinner(f'Sniper analisando {ticker}...'):
        try:
            # NOVO: Adicionando cabeçalho para evitar bloqueio
            acao = yf.Ticker(t_full)
            
            # Força a busca dos dados históricos primeiro
            hist = acao.history(period="1mo")
            
            if hist.empty:
                st.error(f"Sem dados para '{ticker}'. Tente o código (ex: BBDC4)")
            else:
                # Tenta pegar as info fundamentais
                info = acao.info
                preco_atual = hist['Close'].iloc[-1]
                
                vpa = info.get('bookValue', 0)
                lpa = info.get('trailingEps', 0)
                
                st.subheader(f"Análise de {ticker}")
                
                if vpa and lpa and vpa > 0 and lpa > 0:
                    valor_graham = math.sqrt(22.5 * vpa * lpa)
                    margem = ((valor_graham - preco_atual) / preco_atual * 100)
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Preço Atual", f"R$ {preco_atual:.2f}")
                    col2.metric("Preço Justo (Graham)", f"R$ {valor_graham:.2f}", f"{margem:.1f}%")
                    
                    if valor_graham > preco_atual:
                        st.success(f"🎯 OPORTUNIDADE: Margem de {margem:.1f}%")
                    else:
                        st.warning("⚖️ ATIVO ACIMA DO PREÇO JUSTO")
                else:
                    st.info("Nota: VPA/LPA não disponíveis. Exibindo apenas cotação.")
                    st.metric("Preço Atual", f"R$ {preco_atual:.2f}")
                
                # Gráfico
                st.line_chart(hist['Close'])
                    
        except Exception:
            st.error("O mercado está demorando a responder. Tente novamente em 10 segundos.")