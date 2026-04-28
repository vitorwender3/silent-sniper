import streamlit as st
import yfinance as yf
import math
import plotly.graph_objects as go

st.set_page_config(page_title="Silent Sniper Pro", page_icon="🎯", layout="centered")

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
                    lpa = info.get('trailingEps', 0) or 0
                    pvp = info.get('priceToBook', 0) or 0
                    
                    # Lógica de correção do DY
                    raw_dy = info.get('dividendYield', 0) or 0
                    if raw_dy > 1:
                        dy = raw_dy / 100
                    elif 0 < raw_dy < 1:
                        dy = raw_dy * 100
                    else:
                        dy = raw_dy

                    valor_graham = math.sqrt(22.5 * vpa * lpa) if (vpa > 0 and lpa > 0) else 0
                    margem = ((valor_graham - preco_atual) / preco_atual * 100) if valor_graham > 0 else 0
                    cor_painel = "#2e7d32" if valor_graham > preco_atual else "#c62828"
                    
                    st.markdown(f"""
                        <div style="background-color: {cor_painel}; padding: 20px; border-radius: 5px; color: white; font-family: monospace; line-height: 1.6;">
                            EMPRESA: {info.get('longName', ticker)}<br>
                            ATIVO: {ticker} | PREÇO: R$ {preco_atual:.2f}<br>
                            --------------------------------------------<br>
                            DY: {dy:.2f}% | P/VP: {pvp:.2f}<br>
                            VPA: {vpa:.2f} | LPA: {lpa:.2f}<br>
                            --------------------------------------------<br>
                            VALOR GRAHAM: R$ {valor_graham:.2f} | MARGEM: {margem:.2f}%<br>
                            🎯 OPORTUNIDADE: {'COMPRA' if valor_graham > preco_atual else 'AGUARDAR'}
                        </div>
                    """, unsafe_allow_html=True)

                    fig = go.Figure()
                    if valor_graham > 0:
                        fig.add_shape(type="line", x0=hist.index[0], y0=valor_graham, x1=hist.index[-1], y1=valor_graham,
                                    line=dict(color="green", width=2, dash="dash"))
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', line=dict(color='#58a6ff', width=3)))
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0), 
                                    height=300, title=dict(text=f"TENDÊNCIA 30D: {ticker}", x=0.5, font=dict(color="white", size=14)),
                                    xaxis=dict(showgrid=True, gridcolor='#333', griddash='dot'),
                                    yaxis=dict(showgrid=True, gridcolor='#333', griddash='dot'), showlegend=False)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            except Exception:
                st.error("Erro na conexão. Verifique o código do ativo.")