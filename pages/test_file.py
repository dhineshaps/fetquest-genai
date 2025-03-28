import pandas as pd
import streamlit as st
import sys

# for key in list(st.session_state.keys()):
#     del st.session_state[key]


df1 = pd.read_csv("/mount/src/fetquest-genai/sectoral_data_companies.csv", index_col=0)
df2 = pd.read_csv("/mount/src/fetquest-genai/All_Stocks_Data.csv")

# df2['BSE_Symbol'] = pd.to_numeric(df2['BSE_Symbol'], errors='coerce')
# df2['BSE_Symbol'] = df2['BSE_Symbol'].fillna(0).astype(int)
# # df2['BSE_Symbol'] = pd.to_numeric(df2['BSE_Symbol'], errors='coerce').fillna(0).astype(int)
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
        # selected_value = st.selectbox("Select a Company:", filtered_values,index=None,placeholder="ITC",)
        # st.session_state["selected_company"] = selected_value
        # val = st.button("Proceed",type="primary")
        # if val:
        #     if(selected_value): 
        #        cos = selected_value
        #     else:
        #         st.write("Please select the Stock continue")
        #         st.stop()
        #     try:
        #        scrip = df2.loc[df2['Name of the Company'] == cos, 'NSE_Symbol'].item()
        #        market="NSE"
        #     except:
        #        scrip = None
        #     if pd.isna(scrip):
        #     #if(scrip):
        #         st.write("nse is empty")
        #         try:
        #           scrip = df2.loc[df2['Name of the Company'] == cos, 'BSE_Symbol'].item()
        #           market="BSE"
        #         except:
        #             st.write("Unfrtunately can't fulfill the request for given cos, write to fetquest")
        #             st.stop()
        #     st.write("Script is ",scrip)
        #     # st.session_state["data"] = {"cos": cos, "scrip": scrip,"market":market}
        #     # if(scrip):
        #     #      st.switch_page("pages/1_AI_Stock_Screener.py")
        # #st.write(f"Stored in session: {st.session_state['selected_company']}")
        # filtered_df = df1[[select_column]].replace("", pd.NA).dropna()
        # st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("No companies available for this sector.")

#print(df2)