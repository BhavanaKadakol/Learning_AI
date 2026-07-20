# from openai import OpenAI
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()
import requests

client = AzureOpenAI(
   #  api_key=os.getenv("GEMINI_API_KEY"),
   #  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

    # api_key=os.getenv("OPEN_AI_KEY"),
    # base_url="https://openrouter.ai/api/v1"

    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint="https://km-whisper.openai.azure.com",
    api_version="2025-01-01-preview"

)

def get_weather(city: str):
    url=f"https://wttr.in/{city}?format=%c+%t"
    responce =requests.get(url)
    if responce.status_code == 200:
        return responce.text
    else:
        return "Weather data not available"
    
available_tools={
    "get_weather":get_weather
}
SYSTEM_PROMPTS ="""Your are an expert AI assistant you need to solve the problems using chain of thoughts.
To solve any kind of problem related to science, travel, technology, or any concepts, you will be answering in steps: START, PLAN, OUTPUT.
Firstly you need to think about the question and plan it out, then you need to answer it.
if you want you can call the tools if neccessry fro available tools.
For every tool call wait for the OBESERVE step which is the output from the tool call.

Available tools: get_weather , where the fuction or tool give the weather of the city you provide.

Rules:
- The output MUST be a valid JSON object.
- Strictly run ONE step at a time per response. Do not output multiple steps at once.
- START: what the question is about, PLAN: how you are going to answer the question,or TOOL: Any function that can be used to answer the question, OUTPUT: the answer to the question

You must format your response exactly as a JSON object like this:
{"STEP": "START", "CONTENT": "<Your content here>"}

Example1 sequence:
{"STEP": "START", "CONTENT": "User is asking why the sky is blue."}
{"STEP": "PLAN", "CONTENT": "I will explain Rayleigh scattering."}
{"STEP": "OUTPUT", "CONTENT": "The sky is blue because of Rayleigh scattering..."}

Example2 sequence:
{"STEP": "START", "CONTENT": "User is asking about the weather in hubli."}
{"STEP": "PLAN", "CONTENT": "I will get the weather of hubli."}
{"STEP": "TOOL", "CONTENT": "get_weather(\"hubli\")"}
{"STEP": "OBSERVE", "CONTENT": "TOOL": get_weather,"OUTPUT":"The weather in hubli is cloudy with a temperature of 25 degrees Celsius.}
{"STEP": "OUTPUT", "CONTENT": "The weather in hubli is cloudy with a temperature of 25 degrees Celsius."}

"""

message_history = [{"role": "system", "content": SYSTEM_PROMPTS}]

user_input = input("Enter your question: ")
message_history.append({"role":"user", "content":user_input})


while True:
    response = client.chat.completions.create(
    # model="deepseek/deepseek-v3.2-exp",
    model="gpt-4o-mini",
    response_format= {"type":"json_object"},
    messages=message_history
    )

    raw_results=response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_results})
    final_results=json.loads(raw_results)
    
    # If response is a list, take first item
    if isinstance(final_results, list):
        final_results = final_results[0]

    if final_results.get("STEP")=="START":
       print("Started: ",final_results.get("CONTENT"))
       continue
    if final_results.get("STEP")=="TOOL":
       tool_call=final_results.get("tool")
       tool_input = final_results.get("input")
       print(f"\tTool: {tool_call}({tool_input})")

       tool_responce =available_tools[tool_call](tool_input)
       message_history.append({"role":"developer","content":json.dumps(
        {"step":"OBSERVE","tool": tool_call,"input":tool_input,"output":tool_responce }
       )})
       continue
    if final_results.get("STEP")=="PLAN":
       print("PLAN: ",final_results.get("CONTENT"))
       continue
    if final_results.get("STEP")=="OUTPUT":
       print("OUTPUT: ",final_results.get("CONTENT"))
       break
