from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool, set_tracing_disabled
from tavily import TavilyClient
import os
from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI

# Load env
load_dotenv()
#print(os.getenv("GEMINI_API_KEY"))
#print(os.getenv("TAVILY_API_KEY"))
gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Tavily client
tavily_client = TavilyClient(api_key=tavily_api_key)
set_tracing_disabled(True)  

# Wrap Tavily search as a function_tool
@function_tool
def web_search(query: str) -> str:
    """Search the web using Tavily API and return summarized results."""
    results = tavily_client.search(query)
    return str(results)

# Gemini external client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

#config = RunConfig(
    #model=model,
    #model_provider=external_client,
   # tracing_disabled=True
#)

# Agent with Tavily search tool
web_agent = Agent(
    name="websearch_tool_agent",
    instructions="You are a helpful AI agent that can search and extract information using Tavily.",
    tools=[web_search],   # custom tool
    model=model
)


async def main():
 result = await Runner.run(
    web_agent,
  
    input="Who is Lionel Messi?"
    
)

 print("Final Result:", result)

if __name__ == "__main__":
    asyncio.run(main())