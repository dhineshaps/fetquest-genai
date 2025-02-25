from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.googlesearch import GoogleSearch
from dotenv import load_dotenv
import time
from typing import Iterator 
from phi.run.response import RunEvent, RunResponse

load_dotenv()

web_search_agent = Agent(
    name="Web Agent",
    description="This is the agent for searching content from the web",
    role="Search the web for the information",
    model=Groq(id="llama-3.2-11b-vision-preview"),
    tools=[
        GoogleSearch(fixed_language='english', fixed_max_results=5),
        DuckDuckGo(fixed_max_results=5)],
    instructions=['Always include sources and verification'],
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    description="Your task is to find the finance information",
    role="Providing financial insights",
    model=Groq(id="llama-3.2-11b-vision-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Use tables to display data"],
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

# CAL  = web_search_agent.print_response("recent news about ITC", stream=True)
# time.sleep(2.5)
# MAL = CAL  = finance_agent.print_response("Provide a fundamental analysis for ITC.NS", stream=True)

# query = ("Provide a fundamental analysis for ITC.NS")
# response = multi_ai_agent.print_response(query, stream=True)


def as_stream(response):
  for chunk in response:
    if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
      if chunk.event == RunEvent.run_response:
        yield chunk.content
