import os
import requests
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, RunConfig, function_tool, OpenAIChatCompletionsModel, set_tracing_disabled

# Load environment
load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

print("GEMINI_API_KEY:", gemini_api_key)
print("WEATHER_API_KEY:", WEATHER_API_KEY)

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
   
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = OpenAIChatCompletionsModel(model="gemini-2.5-flash",openai_client=external_client)

set_tracing_disabled(True)
# -----------------
# Weather Tool
# -----------------
@function_tool
async def get_weather(city: str) -> str:
    """Fetch the current temperature for a given city."""
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        return f"The weather in {city} is {temp_c}°C with {condition}."
    except Exception as e:
        # Mock fallback
        return f"Sorry, could not fetch weather for {city}. (Error: {e})"


# -----------------
# Agent
# -----------------
weather_agent = Agent(
    name="Weather Assistant",
    instructions="You are a weather assistant. If a user asks about the weather in a city, use the weather tool to answer.",
    model=MODEL,
    tools=[get_weather],
)

async def main():
        user_input = "What's the weather in karachi?"
        result = await Runner.run (weather_agent ,user_input)
        print("Final Result:", result)
if __name__ == "__main__":
   
    asyncio.run(main())

