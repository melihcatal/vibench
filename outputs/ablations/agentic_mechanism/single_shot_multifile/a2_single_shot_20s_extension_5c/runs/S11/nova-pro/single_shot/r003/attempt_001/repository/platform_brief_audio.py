import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_briefing(output):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=output
    )
    return response.read()