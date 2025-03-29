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

st.write("Inital Testing")