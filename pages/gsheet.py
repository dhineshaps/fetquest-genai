
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import date

#spreadsheet = "https://docs.google.com/spreadsheets/d/1EZQAoxf6oG9kYaa7pD7xiunJzeQ-TqlsGttIpu4sOa8/edit?gid=0#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)
print(conn) 

# Read data into a DataFrame
df = conn.read(
    worksheet="All_Stocks_Data"
)

df1 = conn.read(
    worksheet="sectoral_data_companies"
)

col_one_list = df['Name of the Company'].tolist()

with st.form("input_form"):
    st.subheader(":green[Select Stock & Date Range to get returns over the period]")
    col1, col2, col3 = st.columns([2, 1, 1])  # Adjusting column width
    
    with col1:
     SCRIP = st.selectbox(
        "Select the Stock Company",
        col_one_list,
        index=None,
        placeholder="ITC",
    )

    with col2:
        start_date = st.date_input("Start", value=date(2023, 1, 1))

    with col3:
        end_date = st.date_input("End", value=date.today())

    proceed = st.form_submit_button("proceed",type="primary")