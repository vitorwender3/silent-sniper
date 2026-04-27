import streamlit as st
import yfinance as yf
import math
import pandas as pd

# Configuração da Página para Celular
st.set_page_config(page_title="Silent Sniper Mobile", page_icon="🎯")

st.markdown("<h1 style='text-align: center; color: #58a6ff;'>SILENT SNIPER PRO</h1>", unsafe_allow_html=True)

ticker = st.text_input("DIGITE O ATIVO (Ex: BBAS3)", "").upper().strip()

if ticker:
    try:
        t_full = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker
        acao = yf.Ticker(t_full)
        hist = acao.history(period="30d")
        info = acao.info
        
        preco = hist['Close'].iloc[-1]
        vpa = info.get('bookValue', 0) or 0
        lpa = info.get('trailingEps', 0) or 0
        
        # Graham
        g = math.sqrt(22.5 * vpa * lpa) if (vpa > 0 and lpa > 0) else 0
        margem = ((g - preco) / preco * 100) if g > 0 else 0

        # Cards de Informação
        col1, col2 = st.columns(2)
        col1.metric("Preço Atual", f"R$ {preco:.2f}")
        col2.metric("Preço Graham", f"R$ {g:.2f}", f"{margem:.1f}%")

        if g > preco:
            st.success(f"🎯 OPORTUNIDADE IDENTIFICADA: {margem:.1f}% de margem")
        else:
            st.warning("⚖️ ATIVO ACIMA DO PREÇO JUSTO")

        # Gráfico Interativo (Já ajustado para toque no celular)
        st.line_chart(hist['Close'])

    except:
        st.error("Erro ao buscar dados. Verifique o código do ativo.")