import streamlit as st
import yfinance as yf
import math

st.set_page_config(page_title="Silent Sniper Pro", page_icon="🎯")

st.markdown("<h1 style='text-align: center; color: #58a6ff;'>SILENT SNIPER PRO</h1>", unsafe_allow_html=True)

# Dicionário de tradução (Apelidos para Tickers)
APELIDOS = {
    "PETROBRAS": "PETR4", "VALE": "VALE3", "BANCO DO BRASIL": "BBAS3",
    "BRADESCO": "BBDC4", "ITAU": "ITUB4", "ITAÚ": "ITUB4",
    "SABESP": "SBSP3", "SANEPAR": "SAPR4", "MAGALU": "MGLU3",
    "AMBEV": "ABEV3", "WEG": "WEGE3", "B3": "B3SA3",
    "EMBRAER": "EMBR3", "GERDAU": "GGBR4", "ELETROBRAS": "ELET3",
    "COZAN": "CSAN3", "LOCALIZA": "RENT3", "CEMIG": "CMIG4",
    "TAEEA": "TAEE11", "AZUL": "AZUL4", "GOL": "GOLL4"
}

# Campo de busca
entrada_usuario = st.text_input("DIGITE O NOME OU O CÓDIGO (Ex: Bradesco ou BBDC4)", "").upper().strip()

if entrada_usuario:
    # Verifica se o usuário digitou um nome que está no nosso dicionário
    ticker = APELIDOS.get(entrada_usuario, entrada_usuario)
    
    with st.spinner(f'Sniper analisando {ticker}...'):
        try:
            # Garante o sufixo .SA para a busca no Yahoo Finance
            t_full = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker
            
            acao = yf.Ticker(t_full)
            hist = acao.history(period="1mo")
            
            if hist.empty:
                st.error(f"Não encontramos dados para '{entrada_usuario}'. Verifique o código.")
            else:
                info = acao.info
                preco_atual = hist['Close'].iloc[-1]
                
                # Dados para Graham (VPA e LPA)
                vpa = info.get('bookValue', 0) or 0
                lpa = info.get('trailingEps', 0) or 0
                
                if vpa > 0 and lpa > 0:
                    valor_graham = math.sqrt(22.5 * vpa * lpa)
                    margem = ((valor_graham - preco_atual) / preco_atual * 100)
                    
                    st.subheader(f"Análise de {ticker}")
                    col1, col2 = st.columns(2)
                    col1.metric("Preço Atual", f"R$ {preco_atual:.2f}")
                    col2.metric("Preço Justo (Graham)", f"R$ {valor_graham:.2f}", f"{margem:.1f}%")
                    
                    if valor_graham > preco_atual:
                        st.success(f"🎯 OPORTUNIDADE IDENTIFICADA: Margem de {margem:.1f}%")
                    else:
                        st.warning("⚖️ ATIVO ACIMA DO PREÇO JUSTO")
                    
                    st.line_chart(hist['Close'])
                else:
                    st.info("Dados de VPA/LPA não encontrados. Exibindo apenas cotação.")
                    st.metric("Preço Atual", f"R$ {preco_atual:.2f}")
                    st.line_chart(hist['Close'])
                    
        except Exception as e:
            st.error("Erro na conexão com o mercado.")