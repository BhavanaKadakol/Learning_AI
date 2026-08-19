from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Hello, how are you?"},
                {"type": "image_url", "image_url": {"url": "https://tse2.mm.bing.net/th/id/OIP.G37tgeQqSNt7v2oPfj9ltQHaE7?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"}}
            ]
        }
    ])

print("Response:", response.choices[0].message.content)