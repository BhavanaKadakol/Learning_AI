from urllib3.util import Url
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPEN_AI_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
    
def get_weather(city: str):
    url=f"https://wttr.in/{city}?format=%c+%t"
    responce =requests.get(url)
    if responce.status_code == 200:
        return responce.text
    else:
        return "Weather data not available"
    



def main():
    user_query = input("input>>>:")
    response = client.chat.completions.create(
        model ="qwen/qwen3-next-80b-a3b-thinking",
        messages = [
            {"role":"user","content":user_query}
        ]
    )

    print(f":{response.choices[0].message.content}")

print(get_weather("hubli"))