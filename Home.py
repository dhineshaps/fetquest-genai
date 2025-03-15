import streamlit as st
from PIL import Image
im = Image.open('the-fet-quest.jpg')
st.set_page_config(page_title="Home", page_icon = im,layout="wide")
left_co, cent_co,last_co = st.columns(3)

with st.sidebar: 
    st.markdown(":blue[Services:]")
    st.sidebar.page_link('pages/1_AI_Stock_Screener.py', label='AI_Stock_Screener')
    st.sidebar.page_link('pages/2_Chatbot.py', label='Chatbot')
    st.sidebar.page_link('pages/3_Imagebot.py', label='Imagebot')
    st.sidebar.page_link('pages/4_Indices_and%20_Interest_Rates.py', label='Indices_and_Interest_Rate')
    st.sidebar.page_link('pages/5_PDF_Report_Analyzer.py', label='PDF_Report_Analyzer')
    st.sidebar.page_link('pages/6_About_us_And_FAQs.py', label='About_us_And_FAQs')
      
with cent_co:
      new_title = '<p style="font-family:fantasy; color:#DAA520; font-size: 42px;">The FET Quest</p>'
      st.markdown(new_title, unsafe_allow_html=True)

left_co1, cent_co1,last_co1= st.columns(3)
with cent_co1:
      new_title1 = '<h6 style="font-family:cursive; color:#DAA520; font-size: 15px;">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;- Embracing the Financial Literacy</h6>'
      st.markdown(new_title1, unsafe_allow_html=True)

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


st.write('_The FET Quest_ is committed to simplifying Finance and creating value for our esteemed clients in making their investment decisions.')

st.markdown("<h6 style='text-align: left;color:DarkKhaki;'><em>\"You don't have to be brilliant, only a little bit wiser than the other guys, on average, for a long, long, time - Charlie Munger\"</em></h6>", unsafe_allow_html=True)

st.write('Investment instruments continue to bewilder individuals with their financial jargon, we are envisioned to untangle it by Integrating it with technology and making life simple.')

st.write('we are working on services that include Financial Valuation of the Equity Markets and AI-powered Annual Financial Report Analyser,Intercepting Balance Sheets of the company which saves huge time in evaluating the cos.')

st.write(':blue[Many more yet to come - Passionate to keep things Simple.]')
