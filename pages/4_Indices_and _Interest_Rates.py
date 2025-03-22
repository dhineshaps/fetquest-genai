from nsepython import *
import json 
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

from PIL import Image
im = Image.open('the-fet-quest.jpg')
st.set_page_config(page_title="Indices", page_icon = im,layout="wide")

with st.sidebar:
    st.sidebar.page_link('pages/homepage.py', label='Home') 
    st.markdown(":blue[Services:]")
    st.sidebar.page_link('pages/1_AI_Stock_Screener.py', label='AI Stock Screener')
    st.sidebar.page_link('pages/sectoral_stock.py', label='Sectoral Stocks')
    st.sidebar.page_link('pages/2_Chatbot.py', label='Chatbot')
    st.sidebar.page_link('pages/3_Imagebot.py', label='Imagebot')
    st.sidebar.page_link('pages/4_Indices_and _Interest_Rates.py', label='Indices and Interest_Rate')
    st.sidebar.page_link('pages/5_PDF_Report_Analyzer.py', label='PDF Report Analyzer')
    st.sidebar.page_link('pages/6_About_us_And_FAQs.py', label='About us And FAQs')
    st.divider()
    st.sidebar.image("the-fet-quest.jpg")

left_co, cent_co,last_co = st.columns(3)
with cent_co:
      new_title = '<p style="font-family:fantasy; color:#DAA520; font-size: 32px;">Indices and Interest rates 📈</p>'
      st.markdown(new_title, unsafe_allow_html=True)


footer="""<style>
#MainMenu {visibility: hidden; }
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤️ By The FET Quest<a style='display: block; text-align: center</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
st.sidebar.image("the-fet-quest.jpg")
st.info("Live Market Indices are getting Feed Except on Market Holidays")
st.header(":violet[Nifty Major Indices]",anchor=False)

n50 = nse_get_index_quote("nifty 50").get('last')
n50change = nse_get_index_quote("nifty 50").get('percChange') + "%"

nbank = nse_get_index_quote("NIFTY BANK").get('last')
nbankchange = nse_get_index_quote("NIFTY BANK").get('percChange') + "%"

nIT = nse_get_index_quote("NIFTY IT").get('last')
nITchange = nse_get_index_quote("NIFTY IT").get('percChange') + "%"
col1,col2,col3= st.columns(3)

col1.metric(label="Nitfy 50", value=n50,delta=n50change)
col2.metric(label="Nitfy Bank", value=nbank,delta=nbankchange)
col3.metric(label="Nitfy IT", value=nIT,delta=nITchange)

st.divider()

st.header(":violet[Government Investment Instruments and Interest Rates]",anchor=False)
colnames = ['Investment Scheme', 'Interest Rate',' Benefits', 'Lock-in Period', 'Minimum Investment',' Maximum Investment']

df = pd.read_csv('/mount/src/fetquest-genai/investment_int_rates.csv', names=colnames)
st.info("Feel Free to drag and create filter over the table")
AgGrid(df)
st.warning("Interest Rate are not fixed and periodically changed by the Government, Please act on it accordingly")
