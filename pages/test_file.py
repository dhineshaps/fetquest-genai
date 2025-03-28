import pandas as pd
import streamlit as st
import sys
from st_aggrid import AgGrid, GridOptionsBuilder
# for key in list(st.session_state.keys()):
#     del st.session_state[key]

"""
try:
    df1 = pd.read_csv("/mount/src/fetquest-genai/sectoral_data_companies.csv", index_col=0)
    df2 = pd.read_csv("/mount/src/fetquest-genai/All_Stocks_Data.csv")
except FileNotFoundError as e:
    st.error(f"Error loading data: {e}")
    sys.exit()
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
    if select_column in df1.columns:
          filtered_values = df1[select_column].replace("", pd.NA).dropna().tolist()
    else:
        st.error(f"Error: The selected column '{select_column}' does not exist in df1.")
        st.stop()
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
        filtered_df = df1[[select_column]].replace("", pd.NA).dropna()
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True)
        else:
             st.warning("No data available for the selected sector.")

#print(df2)
"""

df = pd.read_csv("/mount/src/fetquest-genai/sectoral_data_companies.csv", index_col=0)

st.subheader("Data Preview")
#AgGrid(df)
selected_column = st.selectbox("Select a column", df.columns)
if selected_column:
    # Get unique values of the selected column
    unique_values = df[selected_column].dropna().unique()
    
    # Display unique values in AgGrid
    st.subheader(f"Unique values in {selected_column}")
    unique_df = pd.DataFrame({selected_column: unique_values})
    
    # Configure Grid Options
    gb = GridOptionsBuilder.from_dataframe(unique_df)
    gb.configure_default_column(width=200)
    grid_options = gb.build()
    
    # Display AgGrid with reduced height
    AgGrid(unique_df, gridOptions=grid_options, fit_columns_on_grid_load=True, height=300)