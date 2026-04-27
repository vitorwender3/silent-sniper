import streamlit as st
import yfinance as yf
import math
import plotly.graph_objects as go

st.set_page_config(page_title="Silent Sniper Pro", page_icon="🎯", layout="centered")

# CSS para estilo Dark Pro
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button { width: 100%; background-color: #2e7d32; color: white; border-radius: 5px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #58a6ff; font-family: sans-serif;'>SILENT SNIPER PRO</h1>", unsafe_allow_html=True)

APELIDOS = {
    "PETROBRAS": "PETR4", "VALE": "VALE3", "BANCO DO BRASIL": "BBAS3",
    "BRADESCO": "BBDC4", "ITAU": "ITUB4", "ITAÚ": "ITUB4",
    "SABESP": "SBSP3", "SANEPAR": "SAPR4", "MAGALU": "MGLU3",
    "AMBEV": "ABEV3", "WEG": "WEGE3", "B3": "B3SA3"
}

entrada = st.text_input("", placeholder="DIGITE O ATIVO (Ex: BBAS3)").upper().strip()

if entrada:
    ticker = APELIDOS.get(entrada, entrada)
    t_full = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker
    
    try:
        acao = yf.Ticker(t_full)
        hist = acao.history(period="2mo") # Pegamos 2 meses para ter folga no gráfico
        
        if not hist.empty:
            info = acao.info
            preco_atual = hist['Close'].iloc[-1]
            vpa = info.get('bookValue', 0)
            lpa = info.get('trailingEps', 0)
            dy = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
            pvp = info.get('priceToBook', 0)

            # Cálculo Graham
            valor_graham = math.sqrt(22.5 * vpa * lpa) if (vpa > 0 and lpa > 0) else 0
            margem = ((valor_graham - preco_atual) / preco_atual * 100) if valor_graham > 0 else 0

            # Painel Verde de Informações (Igual ao Desktop)
            status_cor = "#2e7d32" if valor_graham > preco_atual else "#c62828"
            st.markdown(f"""
                <div style="background-color: {status_cor}; padding: 20px; border-radius: 5px; color: white; font-family: monospace; line-height: 1.6;">
                    ATUAL: {ticker} | PREÇO: R$ {preco_atual:.2f}<br>
                    --------------------------------------------<br>
                    DY: {dy:.2f}% | P/VP: {pvp:.2f}<br>
                    VPA: {vpa:.2f} | LPA: {lpa:.2f}<br>
                    --------------------------------------------<br>
                    VALOR GRAHAM: R$ {valor_graham:.2f} | MARGEM: {margem:.2f}%<br>
                    🎯 OPORTUNIDADE: {'COMPRA' if valor_graham > preco_atual else 'AGUARDAR'}
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"<p style='text-align: center; color: white; margin-top: 20px;'>TENDÊNCIA 30D: {ticker}</p>", unsafe_allow_html=True)

            # --- GRÁFICO IGUAL AO DESKTOP ---
            fig = go.Figure()

            # Linha de Preço Justo (Verde Pontilhada)
            if valor_graham > 0:
                fig.add_shape(type="line", x0=hist.index[0], y0=valor_graham, x1=hist.index[-1], y1=valor_graham,
                            line=dict(color="green", width=2, dash="dash"))
                fig.add_annotation(x=hist.index[5], y=valor_graham, text=f"Justo: R${valor_graham:.2f}", 
                                 showarrow=False, font=dict(color="green"), yshift=10)

            # Linha de Preço (Azul)
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', line=dict(color='#58a6ff', width=3)))

            # Marcadores de Início e Fim (Bolinhas Vermelha/Verde)
            fig.add_trace(go.Scatter(x=[hist.index[0]], y=[hist['Close'].iloc[0]], mode='markers', marker=dict(color='red', size=10)))
            fig.add_trace(go.Scatter(x=[hist.index[-1]], y=[hist['Close'].iloc[-1]], mode='markers', marker=dict(color='lightgreen', size=10)))

            # Layout Dark do Gráfico
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0), height=300,
                xaxis=dict(showgrid=True, gridcolor='#333', gridwidth=1, griddash='dot', showticklabels=True),
                yaxis=dict(showgrid=True, gridcolor='#333', gridwidth=1, griddash='dot'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    except Exception as e:
        st.error("Erro na conexão com o mercado.")