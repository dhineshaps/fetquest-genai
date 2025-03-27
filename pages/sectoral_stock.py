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


df1 = pd.read_csv("/mount/src/fetquest-genai/sectoral_data_companies.csv", index_col=0)
df2 = pd.read_csv("/mount/src/fetquest-genai/All_Stocks_Data.csv")

#conveerting bse symbols to Int from float
df2['BSE_Symbol'] = pd.to_numeric(df2['BSE_Symbol'], errors='coerce').fillna(0).astype(int)


if "Unnamed: 0" in df1.columns:
    df1 = df1.drop(columns=["Unnamed: 0"])

df1.index = range(1, len(df1) + 1)
df1 = df1.fillna('')
clm_name = df1.columns.tolist()

select_column = st.selectbox("Select a sector:", clm_name)

if select_column:
    st.write(f"Selected Sector: {select_column}")
    filtered_values = df1[select_column].replace("", pd.NA).dropna().tolist()
    if filtered_values:
        selected_value = st.selectbox("Select a Company:", filtered_values,index=None,placeholder="ITC",)
        st.session_state["selected_company"] = selected_value
        val = st.button("Proceed",type="primary")
        if val:
            if(selected_value): 
               cos = selected_value
               st.write(cos)
            else:
                st.write("Please select the Stock continue")
                st.stop()
            try:
               scrip = df2.loc[df2['Name of the Company'] == cos, 'NSE_Symbol'].item()
               market="NSE"
            except:
               scrip = None
            if pd.isna(scrip):
            #if(scrip):
                #st.write("nse is empty")
                try:
                  scrip = df2.loc[df2['Name of the Company'] == cos, 'BSE_Symbol'].item()
                  market="BSE"
                except:
                    st.write("unfortunately can't fulfill the request for given company, write to fetquest")
                    st.stop()
            #st.write("Script is ",scrip)
            st.session_state["data"] = {"cos": cos, "scrip": scrip,"market":market}
            if(scrip):
                 st.switch_page("pages/1_AI_Stock_Screener.py")
        #st.write(f"Stored in session: {st.session_state['selected_company']}")
        filtered_df = df1[[select_column]].replace("", pd.NA).dropna()
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("No companies available for this sector.")