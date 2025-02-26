import subprocess
subprocess.run(["pip", "install", "--upgrade", "duckduckgo-search"])
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from phi.agent.agent import Agent
from phi.model.groq import Groq
from phi.run.response import RunEvent, RunResponse
from phi.tools.yfinance import YFinanceTools
#from phi.tools.duckduckgo import DuckDuckGo
from duckduckgo_search import *
from phi.tools.googlesearch import GoogleSearch


# Define Web Search Agent
web_search_agent = Agent(
    name="Web Agent",
    description="Searches the web for information",
    role="Search the web as Equity Research Analyst ",
    model=Groq(id="llama-3.2-11b-vision-preview"),
    tools=[
        GoogleSearch(fixed_language='english', fixed_max_results=5)
        #DuckDuckGo(fixed_max_results=5)
    ],
    #instructions="Always include the sources",
     instructions=[
    "For a given topic, search for the top 5 links.",
    "Then read each URL and extract the article text.",
    "Analyse and prepare 3-5 bullet points based on the information.",
   ],
    show_tool_calls=True,
    markdown=True,
)

# Define Finance Agent
finance_agent = Agent(
    name="Finance Agent",
    description="Provides financial insights",
    role="Providing financial insights",
    model=Groq(id="llama-3.2-11b-vision-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True,
                         company_news=True, historical_prices=True)],
    instructions=["Provide detailed analysis"],
    show_tool_calls=True,
    markdown=True,
)


multi_ai_agent = Agent(
    name='A Stock Market Agent',
    role='A comprehensive assistant specializing in stock market analysis',
    model=Groq(id="llama-3.2-11b-vision-preview"),
    team=[web_search_agent, finance_agent],
    instructions=["Provide comprehensive analysis with multiple data sources"],
    show_tool_calls=True,
    markdown=True
)

def as_stream(response):
    """Yields AI-generated responses as a stream."""
    for chunk in response:
        if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
            if chunk.event == RunEvent.run_response:
                yield chunk.content

