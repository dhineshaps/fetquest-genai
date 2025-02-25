import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plot
from urllib.request import urlopen, Request
import traceback
from PIL import Image
from datetime import date
from jugaad_data.nse import stock_df
from datetime import timedelta
from utils.agent_ai import finance_agent,multi_ai_agent,web_search_agent, as_stream

im = Image.open('the-fet-quest.jpg')
st.set_page_config(page_title="Stock_Data", page_icon = im,layout="wide")

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
st.sidebar.image("the-fet-quest.jpg")
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

df = pd.read_csv('/mount/src/fetquest-genai/stock_list.csv')  #data is taken from NSE https://www.nseindia.com/market-data/securities-available-for-trading
col_one_list = df['Symbol'].tolist()

SCRIP = st.selectbox(
   "Enter the Stock Symbol",
   col_one_list,
   index=None,
   placeholder="ITC",
) 


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

def promoter_holdings():
     promoter_holding,Headers = table_extraction(soup,'shareholding','data-table')
     promoter_holding.drop(promoter_holding.tail(1).index,inplace=True)
     sharehold_last_qtr = Headers[-1]
     print(sharehold_last_qtr)
     promoter_holding[sharehold_last_qtr] = promoter_holding[sharehold_last_qtr].astype(float)
     df1 = promoter_holding[['Type', sharehold_last_qtr]]    
     return df1,sharehold_last_qtr

def sales_nums():
     table_df,qtrs = table_extraction(soup,'quarters','data-table')
     df2 = table_df.loc[[0]]
     row_list = df2.loc[[0]].values.flatten().tolist()
     heads =qtrs[1:]
     num_row = [float(i) for i in row_list[1:]]   
     return num_row,qtrs

def eps_nums():
     table_df,qtrs = table_extraction(soup,'quarters','data-table')
     df3 = table_df.loc[[10]]
     row_list = df3.loc[[10]].values.flatten().tolist()
     heads =qtrs[1:]
     num_row = [float(i) for i in row_list[1:]]
     cols = heads
     for i in cols:
            month = i.split(" ")[0]
            years = int(i.split(" ")[1]) 
            if month == 'Jun':
                 mon = 6
                 date1 = 30
            elif month == 'Sep':
                 mon = 9
                 date1 = 30
            elif month == 'Dec':
                 mon =12
                 date1 = 31
            else:
                 mon = 3
                 date1 = 31
            d = date(years, mon, date1)
            daywork =  d.strftime("%A")
            if daywork == 'Saturday':
                nd = d - timedelta(days = 1)
                stocks_data.append(nd)
            elif daywork == 'Sunday':
                nd = d - timedelta(days = 2)
                stocks_data.append(nd)
            else:
                stocks_data.append(d)
     num_row = [float(i) for i in row_list[1:]]
     ltp_row = ltp_extraction()
     return ltp_row, num_row, qtrs


def opm_nums():
     table_df,qtrs = table_extraction(soup,'quarters','data-table')
     df4 = table_df.loc[[3]]
     row_list = df4.loc[[3]].values.flatten().tolist()
     heads =qtrs[1:]
     num_row = [float(i) for i in row_list[1:]]
     print(num_row)
     return num_row, qtrs

#def output_display(pr_hld,qtr,sales,qtrs,eps,qtrss,ltpv,opm,qts):
def output_display(pr_hld,qtr,sales,qtrs,opm,qts):
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
    c4, c5 = st.columns(2)

    with c4:
        st.write(':blue[Share Holding Pattern]')
        x = pr_hld['Type']
        y = pr_hld[qtr]
        fig, ax = plot.subplots(figsize=(12,3.5))
        ax.stem(x, y)
        plot.xlabel("Type of Shareholders")
        plot.ylabel("in %")
        st.pyplot(fig)
        st.info("Higher the Promoter Holding, Higher the Trust in the Company by Owners, however some exception are there" )
    with c5:        
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

    c7, c8 = st.columns(2)
    
    # with c7:
    #     st.write(':blue[Earning Per Share]')
    #     fig3, ax3= plot.subplots(figsize=(12,3.5))
    #     x2 =  qtrss[1:]
    #     y2 = eps
    #     ax3.stem(x2, y2)
    #     plot.xlabel("Quaters")
    #     plot.ylabel("EPS in Rs.")
    #     st.pyplot(fig3)
    #     st.info("Increasing in EPS is good sign")
    
    with c7:
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
def agent_ai(scrip)
      with st.container():    
           st.write("Space for Agentic Container" + scrip)


if(SCRIP):
       link = f'https://www.screener.in/company/{SCRIP}'
       hdr = {'User-Agent':'Mozilla/5.0'}
       req = Request(link,headers=hdr)
try:
      page=urlopen(req)
      soup = BeautifulSoup(page)
      pr_hld,qtr= promoter_holdings()
      sales,qtrs = sales_nums()
      #ltpv,eps,qtrss= eps_nums()
      opm,qts= opm_nums()
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
      output_display(pr_hld,qtr,sales,qtrs,opm,qts)
      agent_ai(SCRIP)
except Exception:
      traceback.print_exc()
      print(f'EXCEPTION THROWN: UNABLE TO FETCH DATA FOR {SCRIP}')

st.info("Watch out this space for more updates")
