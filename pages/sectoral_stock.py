import pandas as pd
import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv
from utils.agent_ai import finance_agent,multi_ai_agent,web_search_agent, as_stream
from st_aggrid import AgGrid,GridOptionsBuilder
from streamlit_gsheets import GSheetsConnection
from supabase import create_client, Client

    
from PIL import Image
im = Image.open('the-fet-quest.jpg')
st.set_page_config(page_title="sectoral_stocks", page_icon = im,layout="wide")


for key in list(st.session_state.keys()):
    del st.session_state[key]


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


# df1 = pd.read_csv("/mount/src/fetquest-genai/sectoral_data_companies.csv", index_col=0)
# df2 = pd.read_csv("/mount/src/fetquest-genai/All_Stocks_Data.csv")

# conn = st.connection("gsheets", type=GSheetsConnection)

# df1 = conn.read(
#     worksheet="sectoral_data_companies",index_col=0
# )

# df2 = conn.read(
#     worksheet="All_Stocks_Data"
# )


########################################Supabase Database Connection for sectoral ##########################################
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

response = supabase.table("sectoral_data_companies").select("*").execute()
data = response.data

df = pd.DataFrame(data)

pivot_df = df.groupby("industry")["company"].apply(list).to_dict()
max_len = max(len(companies) for companies in pivot_df.values())
normalized = {k: v + [None]*(max_len - len(v)) for k, v in pivot_df.items()}

df1 = pd.DataFrame(normalized)

########################################Supabase Database Connection for All Stock ##########################################

response_all_stock_data = supabase.table("All_Stock_Data").select("*").execute()
data_all_Stock_data= response_all_stock_data.data

df2 = pd.DataFrame(data_all_Stock_data)

##############################################################################################################################

#converting bse symbols to Int from float
df2['BSE_Symbol'] = pd.to_numeric(df2['BSE_Symbol'], errors='coerce').fillna(0).astype(int)


if "Unnamed: 0" in df1.columns:
    df1 = df1.drop(columns=["Unnamed: 0"])

df1.index = range(1, len(df1) + 1)
df1 = df1.fillna('')
clm_name = df1.columns.tolist()

st.markdown('<p style="color: #0000FF; font-size: 20px; font-weight: bold;">Select a sector:</p>', unsafe_allow_html=True)
#AgGrid(df)
selected_column = st.selectbox("Select a sector:", clm_name)
if selected_column:
    filtered_values = df1[selected_column].replace("", pd.NA).dropna().tolist()
    if filtered_values:
        selected_value = st.selectbox("Select a Company to Analysis Further based on below data:", filtered_values,index=None,placeholder="ITC",)
        val = st.button("Proceed",type="primary")
        if val:
            if(selected_value):
                cos = selected_value
            else:
                st.write("Please select the Stock continue")
                st.stop()
            try:
               scrip = df2.loc[df2['Name of the Company'] == cos, 'NSE_Symbol'].item()
               market="NSE"
               #print(scrip)
               #scrip=None  #to test getting BSE Value
            except:
               scrip = None
            if pd.isna(scrip):
                try:
                  scrip = df2.loc[df2['Name of the Company'] == cos, 'BSE_Symbol'].item()
                  market="BSE"
                  print(scrip)
                except:
                    st.write("unfortunately can't fulfill the request for given company, write to fetquest")
                    st.stop()
            st.session_state["data"] = {"cos": cos, "scrip": scrip,"market":market}
            if(scrip):
                 st.switch_page("pages/1_AI_Stock_Screener.py")

    st.markdown(f'<h3 style="color:#FFFF00;">{selected_column} Sectoral Stocks</h3>', unsafe_allow_html=True)        
    # Get unique values of the selected column
    unique_values = df1[selected_column].dropna().unique()
    
    # Display unique values in AgGrid
    #st.subheader(f"List of companies in {selected_column} Sector")
    unique_df = pd.DataFrame({selected_column: unique_values})
    
    # Configure Grid Options
    gb = GridOptionsBuilder.from_dataframe(unique_df)
    gb.configure_default_column(width=200)
    grid_options = gb.build()
    
    # Display AgGrid with reduced height
    AgGrid(unique_df, gridOptions=grid_options, fit_columns_on_grid_load=True, height=300)

def agent_ai_news(scrip):
      st.subheader(f":blue[ 💡 {scrip}  Sector Analysis] ", anchor=None,)
      query = f"Provide a comprehensive analysis for {scrip+" Company"} for stock market research."
      chunks = web_search_agent.run(query, stream=True)
      #filtered_chunks = (chunk for i, chunk in enumerate(as_stream(chunks)) if i >= 2)
      with st.container(border=True,height=400):    
           #st.write("Space for Agentic Container web " + scrip)
           #response = st.write_stream(filtered_chunks)
           response = st.write_stream(as_stream(chunks))
if selected_column:
    agent_ai_news(selected_column)