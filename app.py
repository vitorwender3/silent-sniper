import streamlit as st
import yfinance as yf
import math

st.set_page_config(page_title="Silent Sniper Pro", page_icon="🎯")

st.markdown("<h1 style='text-align: center; color: #58a6ff;'>SILENT SNIPER PRO</h1>", unsafe_allow_html=True)

# Campo de texto
ticker = st.text_input("DIGITE O ATIVO (Ex: BBAS3)", "").upper().strip()

if ticker:
    with st.spinner('Buscando dados no mercado...'):
        try:
            # Adiciona .SA automaticamente se o usuário esquecer
            if not ticker.endswith(".SA"):
                t_full = f"{ticker}.SA"
            else:
                t_full = ticker
                
            acao = yf.Ticker(t_full)
            hist = acao.history(period="1mo")
            
            if hist.empty:
                st.error(f"Não encontramos dados para {ticker}. Verifique se o código está correto.")
            else:
                info = acao.info
                preco = hist['Close'].iloc[-1]
                
                # Pega VPA e LPA (com garantia de não ser None)
                vpa = info.get('bookValue', 0) or 0
                lpa = info.get('trailingEps', 0) or 0
                
                # Cálculo de Graham
                if vpa > 0 and lpa > 0:
                    g = math.sqrt(22.5 * vpa * lpa)
                    margem = ((g - preco) / preco * 100)
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Preço Atual", f"R$ {preco:.2f}")
                    col2.metric("Valor de Graham", f"R$ {g:.2f}", f"{margem:.1f}%")
                    
                    if g > preco:
                        st.success(f"🎯 OPORTUNIDADE: Margem de {margem:.1f}%")
                    else:
                        st.warning("⚖️ ACIMA DO PREÇO JUSTO")
                        
                    st.line_chart(hist['Close'])
                else:
                    st.warning("Dados fundamentais (VPA/LPA) indisponíveis para este ativo.")
        except Exception as e:
            st.error("Erro na conexão. Tente novamente em instantes.")