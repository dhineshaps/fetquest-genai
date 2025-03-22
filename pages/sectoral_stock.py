import pandas as pd
import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv

from PIL import Image
im = Image.open('the-fet-quest.jpg')
st.set_page_config(page_title="sectoral_stocks", page_icon = im,layout="wide")

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

st.header(":violet[Stocks in Sectors:]",anchor=False)

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


df1 = pd.read_csv("/mount/src/fetquest-genai/sectoral_stock_ext.csv", index_col=0)

if "Unnamed: 0" in df1.columns:
    df1 = df1.drop(columns=["Unnamed: 0"])

df1.index = range(1, len(df1) + 1)
df1 = df1.fillna('')
clm_name = df1.columns.tolist()
st.markdown('<p style="color: #0000FF; font-size: 20px; font-weight: bold;">Select a sector:</p>', unsafe_allow_html=True)

select_column = st.selectbox("", clm_name,index=None,placeholder="5G")
if select_column:
    filtered_values = df1[select_column].replace("", pd.NA).dropna().tolist()
    if filtered_values:
        st.markdown(f'<h3 style="color:#FFFF00;">{select_column} Sectoral Stocks</h3>', unsafe_allow_html=True)
        st.markdown("⬇ **Scroll down to view more rows**")
        filtered_df = df1[[select_column]].replace("", pd.NA).dropna()
        st.dataframe(filtered_df, use_container_width=True)