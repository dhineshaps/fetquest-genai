import streamlit as st
from typing import Iterator  # ✅ Fix 1: Import Iterator
from phi.agent import Agent
from phi.model.groq import Groq
#from phi.tools.duckduckgo import DuckDuckGo
from phi.run.response import RunEvent, RunResponse
from phi.tools.googlesearch import GoogleSearch
from phi.tools.yfinance import YFinanceTools


# Define Web Search Agent
web_search_agent = Agent(
    name="Web Agent",
    description="Searches the web for information",
    role="Search the web",
    model=Groq(id="llama-3.2-11b-vision-preview"),
    tools=[
        GoogleSearch(fixed_language='english', fixed_max_results=5)
        #DuckDuckGo(fixed_max_results=5)
    ],
    instructions="Always include the sources",
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

def as_stream(response) -> Iterator[str]:
    """Yields AI-generated responses as a stream."""
    for chunk in response:
        if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
            if chunk.event == RunEvent.run_response:
                yield chunk.content

