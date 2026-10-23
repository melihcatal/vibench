import os

from openai import OpenAI


def localized_audio_preview(text: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return response
