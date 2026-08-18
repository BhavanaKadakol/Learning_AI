from dotenv import load_dotenv
import speech_recognition as sr 
import os
from langchain_openai import AzureChatOpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio
load_dotenv()


model = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)
  
# Initialize recognizer
r = sr.Recognizer()
with sr.Microphone() as source:
   print("Adjusting for ambient noise...")
   r.adjust_for_ambient_noise(source, duration=0.2)
   print("Speak now...")
   audio = r.listen(source)
try:
   text = r.recognize_google(audio)
   print("You said:", text)
except sr.RequestError:
   print("API unavailable")
except sr.UnknownValueError:
   print("Unable to recognize speech")

SYSTEM_PROMPT =""" your are an voice agent. You are gien the transcription of what user said using voice.You need to output as if you are an voice agent and whatever you speak will be coverted to audio using AI and played back to user"""
response = model.invoke([
    ("system", SYSTEM_PROMPT),
    ("user", text)
])

ai_response = response.content

print("AI Response:", ai_response)
async def speak(text):

        openai = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        async with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="coral",
            input=text,
            instructions="Speak in a cheerful and natural tone.",
            response_format="pcm",
        ) as audio_response:

            await LocalAudioPlayer().play(audio_response)


    # -----------------------------
    # 5. Play AI response
    # -----------------------------

asyncio.run(speak(ai_response))
# print("AI Response:", response.choices[0].message.content)

