import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plot
import yfinance as yf
from urllib.request import urlopen, Request
import matplotlib.pyplot as plt
import traceback
from PIL import Image
from datetime import date
#from jugaad_data.nse import stock_df
from datetime import datetime
from datetime import timedelta
from streamlit_gsheets import GSheetsConnection
from supabase import create_client, Client
from utils.agent_ai import finance_agent,multi_ai_agent,web_search_agent, as_stream

im = Image.open('the-fet-quest.jpg')
st.set_page_config(page_title="Stock_Data", page_icon = im,layout="wide")

#      To handle the session variable passed for sectoral data #########################
cos=""
scrip=""
market=""

if "data" in st.session_state:
    #st.write("Session State Variables:")
    cos = st.session_state["data"].get("cos", None)
    scrip = st.session_state["data"].get("scrip", None)
    market= st.session_state["data"].get("market",None)

if not cos or not scrip or not market:  # Check if either 'cos' or 'scrip' is empty/missing
    cos = cos if cos else "dummy"  
    scrip = scrip if scrip else "dummy"
    market = market if market else "dummy"

#   End of to handle the session variable passed for sectoral data #########################

left_co, cent_co,last_co = st.columns(3)
with cent_co:
      new_title = '<p style="font-family:fantasy; color:#DAA520; font-size: 32px;">Stock Screener  📈</p>'
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
#st.sidebar.image("the-fet-quest.jpg")
st.header(":violet[Know About Your Stock:]",anchor=False)
market_cap = 0.0
cmp = 0.0
PE = 0.0
BV = 0.0
sector = " "
industry = " "
PB_Ratio= 0.0
stocks_data = []
LTP = []


#data needs to be handled by multiple ways and compared with latest NSE data
#data is taken from NSE https://www.nseindia.com/market-data/securities-available-for-trading
#df = pd.read_csv("/mount/src/fetquest-genai/All_Stocks_Data.csv")

# conn = st.connection("gsheets", type=GSheetsConnection)

# df = conn.read(
#     worksheet="All_Stocks_Data"
# )


############################Supabase Db Connection###################################
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]

supabase: Client = create_client(url, key)
                                 
@st.cache_data(ttl=3600)
def load_all_stock_data():
    response_all_stock_data = supabase.table("All_Stock_Data").select("*").execute()
    data_all_stock_data = response_all_stock_data.data
    return pd.DataFrame(data_all_stock_data)

######################################################################################
df = load_all_stock_data()
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

today = date.today()
# df = pd.read_csv('/mount/src/fetquest-genai/stock_list.csv')  #data is taken from NSE https://www.nseindia.com/market-data/securities-available-for-trading
# col_one_list = df['SYMBOL'].tolist()

with st.sidebar: 

    # st.header(":green[Select Stock & Date Range to get returns over the period]")
    
    # SCRIP = st.selectbox(
    #     "Select the Stock Symbol",
    #     col_one_list,
    #     index=None,
    #     placeholder="ITC",
    # )

    # start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    # end_date = st.date_input("End Date", value=pd.to_datetime(today))
    # proceed = st.button("Proceed",type="primary")

    #st.divider()
    #st.markdown(":blue[Services:]")
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

def table_extraction(soup, section_id, class_name):
    section_extract = soup.find('section',{'id': section_id})
    table_extract = section_extract.find('table',{'class': class_name})

    col_headers = []
    for header in table_extract.find_all('th'):
        col_headers.append(  header.text or 'Type')

    table_df = pd.DataFrame(columns = col_headers)

    for row_element in table_extract.find_all('tr')[1:]:
            row_data = row_element.find_all('td')
            row = [tr.text.strip() for tr in row_data]
            length = len(table_df)
            table_df.loc[length] = row 

    table_df=table_df.replace('\+','',regex=True)
    table_df=table_df.replace('\%','',regex=True)
    table_df=table_df.replace('\,','',regex=True)        
    return table_df,col_headers

def ltp_extraction():
     #print(stocks_data[0])
     #print(stocks_data[-1])
     print(SCRIP)
     #ltpdf = stock_df(symbol="SBIN", from_date=stocks_data[0],to_date=stocks_data[-1], series="EQ")
     ltpdf = stock_df(symbol=SCRIP, from_date=stocks_data[0],to_date=stocks_data[-1], series="EQ")
     ltpdf['DATE'] = ltpdf['DATE'].astype(str)
     ltpdf['DATE'] = pd.to_datetime(ltpdf['DATE']).dt.date 
     for i in range(len(stocks_data)):
          LTPS = ltpdf.loc[ltpdf['DATE'] == stocks_data[i]]
          col_present = len(LTPS)
          if(col_present == 0):
            while True:
                #print("Here I am")
                cnt = 0
                #print(cnt)
                nd = stocks_data[i] - timedelta(days = 1 + cnt)
                #print(nd)
                #LTPS = df.loc[df['DATE'] == nd, 'LTP'].squeeze()
                LTPS = ltpdf.loc[ltpdf['DATE'] == nd]
                col_present = len(LTPS)
                if(col_present == 1):
                    LTPS = ltpdf.loc[ltpdf['DATE'] == nd, 'LTP'].squeeze()
                    break
                else:
                #print("ere ami in sub lop")
                  cnt = cnt+1
                #print(cnt)
          else:
                #print("inside the escape")    
                LTPS = ltpdf.loc[ltpdf['DATE'] == stocks_data[i], 'LTP'].squeeze()
          LTP.append(LTPS)
     #print(LTP)
     return LTP

def promoter_holdings(soup):
     promoter_holding,Headers = table_extraction(soup,'shareholding','data-table')
     promoter_holding.drop(promoter_holding.tail(1).index,inplace=True)
     sharehold_last_qtr = Headers[-1]
     print(sharehold_last_qtr)
     promoter_holding[sharehold_last_qtr] = promoter_holding[sharehold_last_qtr].astype(float)
     df1 = promoter_holding[['Type', sharehold_last_qtr]]    
     return df1,sharehold_last_qtr

def sales_nums(soup):
     table_df,qtrs = table_extraction(soup,'quarters','data-table')
     df2 = table_df.loc[[0]]
     row_list = df2.loc[[0]].values.flatten().tolist()
     heads =qtrs[1:]
     #num_row = [float(i) for i in row_list[1:]] 
     #to handle the empty space vale if the company don't have data
     num_row = [float(i) if i.replace('.', '', 1).replace('-', '', 1).isdigit() else 0 for i in row_list[1:]]   
     return num_row,qtrs

def eps_nums(soup):
     table_df,qtrs = table_extraction(soup,'quarters','data-table')
     df3 = table_df.loc[[10]]
     row_list = df3.loc[[10]].values.flatten().tolist()
     heads =qtrs[1:]
     #num_row = [float(i) for i in row_list[1:]]
     num_row = [float(i) if i.replace('.', '', 1).replace('-', '', 1).isdigit() else 0 for i in row_list[1:]] 
     # cols = heads
     # for i in cols:
     #        month = i.split(" ")[0]
     #        years = int(i.split(" ")[1]) 
     #        if month == 'Jun':
     #             mon = 6
     #             date1 = 30
     #        elif month == 'Sep':
     #             mon = 9
     #             date1 = 30
     #        elif month == 'Dec':
     #             mon =12
     #             date1 = 31
     #        else:
     #             mon = 3
     #             date1 = 31
     #        d = date(years, mon, date1)
     #        daywork =  d.strftime("%A")
     #        if daywork == 'Saturday':
     #            nd = d - timedelta(days = 1)
     #            stocks_data.append(nd)
     #        elif daywork == 'Sunday':
     #            nd = d - timedelta(days = 2)
     #            stocks_data.append(nd)
     #        else:
     #            stocks_data.append(d)
     # num_row = [float(i) for i in row_list[1:]]
     # ltp_row = ltp_extraction()
     #return ltp_row, num_row, qtrs
     return num_row, qtrs


def opm_nums(soup):
     table_df,qtrs = table_extraction(soup,'quarters','data-table')
     df4 = table_df.loc[[3]]
     row_list = df4.loc[[3]].values.flatten().tolist()
     heads =qtrs[1:]
     #num_row = [float(i) for i in row_list[1:]]
     num_row = [float(i) if i.replace('.', '', 1).replace('-', '', 1).isdigit() else 0 for i in row_list[1:]] 
     print(num_row)
     return num_row, qtrs

def output_stock_data(market_cap,cmp,PE,BV,PB_Ratio,sector):
    c1, c2, c3 = st.columns(3)
    with c1:
         st.write(f':orange[Current Market price -] {cmp} Rs')
         st.write(f':orange[Market Capitilization -] {market_cap} Cr')
    with c2:
        st.write(f':orange[P/E -] {PE}')
        st.write(f':orange[Book Value -] {BV}')
    with c3:
        st.write(f':orange[P/B ratio -] {PB_Ratio}')
        st.write(f':orange[Sector -] {sector.strip()}')
        #st.write(f'Industry : {industry.strip()}')

def agent_ai_fin(scrip):
      st.subheader(f":orange[💹 Fundamental Analyis on {scrip}]" ,anchor=None) 
      query = f"Provide a fundamental analysis for {scrip+".NS"}."
      chunks = finance_agent.run(query, stream=True)
      #filtered_chunks = (chunk for i, chunk in enumerate(as_stream(chunks)) if i >= 3)
      with st.container(border=True,height=400):    
           #st.write("Space for Agentic Container " + scrip)
           #response = st.write_stream(filtered_chunks)
           response = st.write_stream(as_stream(chunks))
            
def agent_ai_news(scrip):
      st.subheader(f":blue[ 💡 Events about {scrip}]", anchor=None,)
      query = f"Provide a comprehensive analysis for {scrip+" Company"} for stock market research."
      chunks = web_search_agent.run(query, stream=True)
      #filtered_chunks = (chunk for i, chunk in enumerate(as_stream(chunks)) if i >= 2)
      with st.container(border=True,height=400):    
           #st.write("Space for Agentic Container web " + scrip)
           #response = st.write_stream(filtered_chunks)
           response = st.write_stream(as_stream(chunks))

def stock_retrun_vs_benchmark(scrip):
    st.subheader(f":blue[ 💲 {cos} vs Indices Return]", anchor=None,)
    d1 = datetime.strptime(str(start_date), "%Y-%m-%d")
    d2 = datetime.strptime(str(end_date), "%Y-%m-%d")
    diff_date=abs((d2.year - d1.year))


    # Define tickers
    ticker_bse = "^BSESN"      # BSE Sensex
    ticker_nse = "^NSEI"       # NSE Nifty 50
    ticker_stock = scrip+".NS"    # Individual Stock (ITC)

    # Fetch data
    data = yf.download(ticker_bse, start=start_date, end=end_date)["Close"]
    data1 = yf.download(ticker_nse, start=start_date, end=end_date)["Close"]
    data2 = yf.download(ticker_stock , start=start_date, end=end_date)["Close"]


    # Combine data into a single DataFrame
    df = pd.concat([data, data1, data2], axis=1)
    df.columns = ["Sensex", "Nifty 50", "Stock"]  # Rename columns
    df = df.dropna()  # Drop rows with missing values

    stock_name = ticker_stock[:-3]
    #print(stock_name)

    # Create Matplotlib figure and axes
    fig1, ax1 = plt.subplots(figsize=(10, 5))

    # First Y-Axis (Sensex)
    ax1.plot(df.index, df["Sensex"], label="Sensex (BSE)", color="blue")
    ax1.set_ylabel("Sensex", color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")
    ax1.grid(True)

    # Second Y-Axis (Nifty 50)
    ax2 = ax1.twinx()
    ax2.plot(df.index, df["Nifty 50"], label="Nifty 50 (NSE)", color="red")
    ax2.set_ylabel("Nifty 50", color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    # Third Y-Axis (Stock)
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Offset third axis
    ax3.plot(df.index, df["Stock"], label=f"Stock {stock_name }", color="green")
    ax3.set_ylabel(f"{stock_name }", color="green")
    ax3.tick_params(axis='y', labelcolor="green")

    # Title and Legend
    ax1.set_xlabel("Date")
    ax1.set_title(f"Sensex vs Nifty 50 & {stock_name } for "+str(diff_date)+ " year")
    fig1.set_size_inches(12, 6)
    fig1.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

    # Display the plot in Streamlit
    # st.pyplot(fig1)
    bse_nback = data.iloc[1,0]
    bse_nprsnt = data.iloc[-1,0]
    bse_diff = round(bse_nprsnt - bse_nback,2) 

    bse_returns = round((bse_diff/bse_nprsnt)*100,2)

    print(bse_returns)

    nse_nback = data1.iloc[1,0]
    nse_nprsnt = data1.iloc[-1,0]
    nse_diff = round(nse_nprsnt - nse_nback,2) 
    nse_returns = round((nse_diff/nse_nprsnt)*100,2)

    print(nse_returns)

    #print(data2)
    stock_nback = data2.iloc[1,0]
    stock_nprsnt = data2.iloc[-1,0]
    stock_diff = round(stock_nprsnt - stock_nback,2) 
    stock_returns = round((stock_diff/stock_nprsnt)*100,2)

    # Plot bar chart
    returns_data = pd.DataFrame({
        "Index": ["Sensex", "Nifty 50", stock_name],
        "Returns (%)": [bse_returns, nse_returns, stock_returns]
    })
    fig, ax = plt.subplots()
    bars = ax.bar(returns_data["Index"], returns_data["Returns (%)"], color=["blue", "green", "red"])
    ax.set_ylabel("Returns (%)")
    ax.set_title(f"Market & Stock Returns Comparison for "+str(diff_date)+ " years")

    # Adding text labels on bars
    for bar, label in zip(bars, returns_data["Returns (%)"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{label}%', ha='center', va='bottom')
    fig.set_size_inches(5, 5)

    with st.expander("Market Performance Charts", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.pyplot(fig1, use_container_width=True)
        with col2:
            st.pyplot(fig, use_container_width=True)

    #st.write(f"{stock_name} returned **{stock_returns}%** ,Nifty 50 returned **{nse_returns}%** and Sensex returned **{bse_returns}%** over **{diff_date}** years.")
    st.markdown(
    f"""
    <h4 style='text-align: center; color: #8E44AD;'>
        {stock_name} returned <span style='font-weight: bold; color: #0000FF;'>{stock_returns}%</span>, 
        Nifty 50 returned <span style='font-weight: bold; color: #0000FF;'>{nse_returns}%</span>, 
        and Sensex returned <span style='font-weight: bold; color: #0000FF;'>{bse_returns}%</span> 
        over <span style='font-weight: bold; color: #0000FF;'>{diff_date}</span> years.
    </h4>
    """,
    unsafe_allow_html=True
)
#def output_display(pr_hld,qtr,sales,qtrs,eps,qtrss,ltpv,opm,qts):
def output_display(pr_hld,qtr,sales,qtrs,opm,qts,eps,qtrss):
    c1, c2 = st.columns(2)

    with c1:
        st.write(':blue[Share Holding Pattern]')
        x = pr_hld['Type']
        y = pr_hld[qtr]
        fig, ax = plot.subplots(figsize=(12,3.5))
        ax.stem(x, y)
        plot.xlabel("Type of Shareholders")
        plot.ylabel("in %")
        st.pyplot(fig)
        st.info("Higher the Promoter Holding, Higher the Trust in the Company by Owners, however some exception are there" )
    with c2:        
        st.write(':blue[Quaterly Sales or Revenue of the company]')
        x1 = sales
        y1 = qtrs[1:]
        fig2, ax2= plot.subplots(figsize=(12,3.5))
        x1 =  qtrs[1:]
        y1 = sales
        ax2.stem(x1, y1)
        plot.xlabel("Quaters")
        plot.ylabel("Sales | Revenue in Rs. crores")
        st.pyplot(fig2)
        st.info("Increasing Sales or Revenue is Good Sign")

    c3,c4  = st.columns(2)
    
    with c3:
        st.write(':blue[Earning Per Share]')
        fig3, ax3= plot.subplots(figsize=(12,3.5))
        x2 =  qtrss[1:]
        y2 = eps
        ax3.stem(x2, y2)
        plot.xlabel("Quaters")
        plot.ylabel("EPS in Rs.")
        st.pyplot(fig3)
        st.info("Increasing in EPS is good sign")
    
    with c4:
        st.write(':blue[Operating Profit Margin]')
        fig4, ax4= plot.subplots(figsize=(12,3.5))
        x3 =  qts[1:]
        y3 = opm
        ax4.stem(x3, y3)
        plot.xlabel("Quaters")
        plot.ylabel("OPM in %")
        st.pyplot(fig4)
        st.info("Operating Profit Margin shows company's Operating profit vs Sales or Revenue")

    #c9,c10,c11= st.columns((1, 5, 1))
    #with c9:

    # with c10:
    #     st.write(':blue[EPS VS Stock Price in Respective Quaters]')
    #     fig5, ax5= plot.subplots(figsize=(15,5.5)) #15,5.5
    #     x3 =  qts[1:]
    #     y3 = eps
    #     y4 = ltpv
    #     color = 'tab:red'
    #     x_color = 'tab:green'
    #     ax5.set_xlabel('Quaters', color=x_color)
    #     ax5.tick_params(axis='x', labelcolor=x_color)
    #     ax5.set_ylabel('EPS in Rs.', color=color)
    #     ax5.plot(x3, y3, color=color, marker='o')
    #     ax5.tick_params(axis='y',labelcolor=color)
    #     ax6 = ax5.twinx()
    #     color = 'tab:blue'
    #     ax6.plot(x3, y4, color=color, marker='o')
    #     ax6.set_ylabel('Stock Price in Rs.', color=color)
    #     ax6.tick_params(axis='y', labelcolor=color)
    #     fig5.tight_layout()
    #     st.pyplot(fig5)
    #     st.info("EPS Increasing along with Price of the stock shows the steady earning and justifiable Stock Price")

def main_flow(SCRIP):
    if(SCRIP):
        link = f'https://www.screener.in/company/{SCRIP}'
        hdr = {'User-Agent':'Mozilla/5.0'}
        req = Request(link,headers=hdr)
    try:
        page=urlopen(req)
        soup = BeautifulSoup(page)
        pr_hld,qtr= promoter_holdings(soup)
        sales,qtrs = sales_nums(soup)
        eps,qtrss= eps_nums(soup) #needs to be commented if below is working but historical stock price is not working
        #ltpv,eps,qtrss= eps_nums()
        opm,qts= opm_nums(soup)
        #print(pr_hld)
        #print("Quater is "+qtr)
        #print(sales)
        div_html = soup.find('div',{'class': 'company-ratios'})
        ul_html = div_html.find('ul',{'id': 'top-ratios'})
        for li in ul_html.find_all("li"):
            name_span = li.find('span',{'class':'name'})
            if 'Market Cap' in name_span.text: 
                num_span = li.find('span',{'class':'number'})
                num_span = num_span.text.replace(',', '')
                market_cap = float(num_span) if (num_span != '') else 0.0
            if ' Current Price' in name_span.text: 
                num_span = li.find('span',{'class':'number'})
                num_span = num_span.text.replace(',', '')
                cmp = float(num_span) if (num_span != '') else 0.0
            if ' Stock P/E' in name_span.text: 
                num_span = li.find('span',{'class':'number'})
                num_span = num_span.text.replace(',', '')
                PE = float(num_span) if (num_span != '') else 0.0
            if ' Book Value' in name_span.text: 
                num_span = li.find('span',{'class':'number'})
                num_span = num_span.text.replace(',', '')
                BV = float(num_span) if (num_span != '') else 0.0
        PB_Ratio = (round(cmp/BV,2))

        div_html1 = soup.find('div',{'class': 'flex flex-space-between'})
        ul_html1 = div_html1.find('p')
        for idx, x in enumerate (ul_html1):
            if(idx == 1):
                for i in x:
                    sector = i
            if(idx == 5):
                for i in x:
                    industry = i 
        #output_display(pr_hld,qtr,sales,qtrs,eps,qtrss,ltpv,opm,qts)
        output_stock_data(market_cap,cmp,PE,BV,PB_Ratio,sector)
        #output_display(pr_hld,qtr,sales,qtrs,opm,qts)
        st.info('AI-powered insights are from complimentary models and Public APIs, please Refresh if the data is not proper', icon="💬")
        if(market=="NSE"):
            agent_ai_fin(SCRIP)
            agent_ai_news(SCRIP)
            stock_retrun_vs_benchmark(SCRIP)
        st.subheader(f":orange[{SCRIP} Financial Performance 📊 ]" ,anchor=None) 
        output_display(pr_hld,qtr,sales,qtrs,opm,qts,eps,qtrss)
    except Exception:
        traceback.print_exc()
        print(f'EXCEPTION THROWN: UNABLE TO FETCH DATA FOR {SCRIP}')

if(proceed):
    if SCRIP is None:
        st.error("Please select a stock symbol before proceeding.")
        st.stop()
    if(SCRIP):
        cos=SCRIP
        scrip_sel = df.loc[df['Name of the Company'] == SCRIP, 'NSE_Symbol'].item()
        market="NSE"
        print(scrip)
        if pd.isna(scrip_sel):
            st.write("nse is empty")
            scrip_sel = int(df.loc[df['Name of the Company'] == SCRIP, 'BSE_Symbol'].item())
            market="BSE"
    with st.spinner("Loading data..."): 
        main_flow(scrip_sel)

if(cos!="dummy" and scrip!="dummy" and market!="dummy"):
    # st.write("not a same page call")
    # st.write(scrip)
    with st.spinner("Loading data..."):
        main_flow(scrip)


st.info("Watch out this space for more updates")
