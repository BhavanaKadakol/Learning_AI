from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model ="gpt-4o-mini",
    messages=[
        {"role":"user","content":"Hello, how are you?"}
    ]
)

print(response.choices[0].message.content)