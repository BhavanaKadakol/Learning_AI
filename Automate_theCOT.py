from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()
client = OpenAI(
   #  api_key=os.getenv("GEMINI_API_KEY"),
   #  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

    api_key=os.getenv("OPEN_AI_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPTS ="""Your are an expert AI assistant you need to solve the problems using chain of thoughts.
To solve any kind of problem related to science, travel, technology, or any concepts, you will be answering in steps: START, PLAN, OUTPUT.
Firstly you need to think about the question and plan it out, then you need to answer it.
pune
Rules:
- The output MUST be a valid JSON object.
- Strictly run ONE step at a time per response. Do not output multiple steps at once.
- START: what the question is about, PLAN: how you are going to answer the question, OUTPUT: the answer to the question

You must format your response exactly as a JSON object like this:
{"STEP": "START", "CONTENT": "<Your content here>"}

Example sequence:
{"STEP": "START", "CONTENT": "User is asking why the sky is blue."}
{"STEP": "PLAN", "CONTENT": "I will explain Rayleigh scattering."}
{"STEP": "OUTPUT", "CONTENT": "The sky is blue because of Rayleigh scattering..."}
"""

message_history = [{"role": "system", "content": SYSTEM_PROMPTS}]

user_input = input("Enter your question: ")
message_history.append({"role":"user", "content":user_input})


while True:
    response = client.chat.completions.create(
    model="qwen/qwen3-next-80b-a3b-thinking",
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
    if final_results.get("STEP")=="PLAN":
       print("PLAN: ",final_results.get("CONTENT"))
       continue
    if final_results.get("STEP")=="OUTPUT":
       print("OUTPUT: ",final_results.get("CONTENT"))
       break
