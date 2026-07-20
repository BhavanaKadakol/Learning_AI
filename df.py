from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# response = client.chat.completions.create(
#     model ="gemini-3-flash-preview",
#     messages=[
#         {"role":"user","content":"Hello, how are you?"}
#     ]
# )

#Zero-shot prompting : you are given the prompt with the question that you have to answer.
# SYSTEM_PROMPTS ="Your a are Travel frek person , you will answer the questions related to the travel and location, not any other thing related questions will be answeredd by you. you can also provide your personal opinions and suggestions related to the travel and location.When you get the other things questions then say sorry in  return."
# response = client.chat.completions.create(
#     model ="gemini-3-flash-preview",
#     messages=[
#         {"role":"system","content":SYSTEM_PROMPTS},
#            { "role":"user","content":"Hello, how are you?"}
#     ]
# )

#few-shot prompting : you are given the prompt with the question that you have to answer. you are also given some examples of the question that you have to answer.
# SYSTEM_PROMPTS ="""Your a are Travel frek person , 
# you will answer the questions related to the travel and location, 
# not any other thing related questions will be answeredd by you. 
# you can also provide your personal opinions and suggestions related to the travel and location.
# When you get the other things questions then say sorry in  return.
# You should answer travel related questions only.

# Your name is Bhavana

# user:Hello, how are you?
# Bhavana: Sorry, I can't answer this question.

# user:Where is the best place to visit in india  ?
# Bhavana: The best place to visit in india is Kashmir.


# """
# response = client.chat.completions.create(
#     model ="gemini-3-flash-preview",
#     messages=[
#         {"role":"system","content":SYSTEM_PROMPTS},
#            { "role":"user","content":"May i know about Kashmir?"}
#     ]
# )

#structured ouput in few shot prompting 
# SYSTEM_PROMPTS ="""Your a are Travel frek person , 
# you will answer the questions related to the travel and location, 
# not any other thing related questions will be answeredd by you. 
# you can also provide your personal opinions and suggestions related to the travel and location.
# When you get the other things questions then say sorry in  return.
# You should answer travel related questions only.

# Your name is Bhavana

# output should be in json format

# {
#     "is_question_relatable":boolean,
#     "answer":string
# }

# user:Hello, how are you?
# Bhavana: {"is_question_relatable":false,
# "answer":"Sorry, I can't answer this question."}

# user:Where is the best place to visit in india  ?
# Bhavana: {"is_question_relatable":true,
# "answer":"The best place to visit in india is Kashmir."}


# """


# COT
SYSTEM_PROMPTS ="""Your are an expert AI assistant you need to slove the problems using chain of thoughts.
 to solve any kind of problem, related to sicence,travel,technology,
anything concepts you will be answering in steps START,PLAN,OUTPUT .
firstly you need to think about the question and plan it out, then you need to answer it.
Steps are : START,PLAN,OUTPUT

Rules:
-The output should be in JSON format.
-Strictly Run one step at a time.
-START : what the question is about,PLAN : how you are going to answer the question,OUTPUT : the answer to the question

{{ STEP: START | PLAN | OUTPUT, CONTENT:"<Answer>"}}

Example:
{{Step: START , CONTENT:User question.}}
{{Step: PLAN, CONTENT:Let user know  what you got from question.}}
{{Step: PLAN, CONTENT:Which area you will categaries the question.}}
{{Step: PLAN, CONTENT:What are your thoughts about the question and how you want to answe it.}}
{{Step: PLAN, CONTENT: What is your thought process about the question}}
{{Step: OUTPUT, CONTENT:Answer the question.}}



"""
response = client.chat.completions.create(
    model ="gemini-3-flash-preview",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system","content":SYSTEM_PROMPTS},
        {"role":"user","content":"What is the capital of india?"},
        # {"role":"assistant","content":json.dumps({"Step": "START", "CONTENT": "The user is asking for the capital city of India."})}    
    ]
)
print(response.choices[0].message.content)