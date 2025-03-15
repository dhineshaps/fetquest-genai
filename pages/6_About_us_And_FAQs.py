import streamlit as st
from PIL import Image
import webbrowser

im = Image.open('the-fet-quest.jpg')
st.set_page_config(page_title="Home", page_icon = im,layout="wide")

with st.sidebar: 
    st.markdown(":blue[Services:]")
    st.sidebar.page_link('pages/1_AI_Stock_Screener.py', label='AI Stock Screener')
    st.sidebar.page_link('pages/2_Chatbot.py', label='Chatbot')
    st.sidebar.page_link('pages/3_Imagebot.py', label='Imagebot')
    st.sidebar.page_link('pages/4_Indices_and _Interest_Rates.py', label='Indices and Interest_Rate')
    st.sidebar.page_link('pages/5_PDF_Report_Analyzer.py', label='PDF Report Analyzer')
    st.sidebar.page_link('pages/6_About_us_And_FAQs.py', label='About us And FAQs')
    st.divider()
    st.sidebar.image("the-fet-quest.jpg")
    
left_co, cent_co,last_co = st.columns(3)
with cent_co:
#    st.title("The FET Quest")
      new_title = '<p style="font-family:fantasy; color:#DAA520; font-size: 42px;">The FET Quest</p>'
      st.markdown(new_title, unsafe_allow_html=True)

left_co1, cent_co1,last_co1= st.columns(3)
with cent_co1:
#    st.title("The FET Quest")
      new_title = '<h6 style="font-family:cursive; color:#DAA520; font-size: 15px;">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Embracing the Financial Literacy</h6>'
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
st.write("Thanks for Visting us, we are happy to hear from you :smiley: !")

st.info("This is model site, we are not recommending any investment instrments or stocks , please do your own research based on the data available here.")

new_title = '<p style="font-family:fantasy; color:#DAA520; font-size: 22px;">FAQs</p>'
st.markdown(new_title, unsafe_allow_html=True)

with st.expander(":mailbox: Reach Us"):
      st.write("Feel Free to write to us :e-mail: daps.investments@gmail.com")
with st.expander("Describe About The FET Quest ?"):
      st.write("The FET Quest is the Educational and Technology subsidiary of :green[DAPS Investments].")
with st.expander("Whether The FET Quest is Registered ?"):
      st.write("We are genuine however this is a Model Technical Portfolio Site, we are not registered under any Sections of Indian Companies Act for now.")
with st.expander("What Benefits The FET Quest can Provide ?"):
      st.write("We offer the First layer of advisory and solutions to your doubts on Financial doubts in Primary and Secondary Markets, Bonds and other Investment Instruments.")

url = 'https://dhinesh-palanisamy.medium.com/'

if st.button('Click here to Visit Medium Blog'):
        webbrowser.open_new_tab(url)