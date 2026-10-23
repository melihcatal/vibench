import os

from openai import OpenAI


def reviewer_brief_audio(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=text
    )
    return response
