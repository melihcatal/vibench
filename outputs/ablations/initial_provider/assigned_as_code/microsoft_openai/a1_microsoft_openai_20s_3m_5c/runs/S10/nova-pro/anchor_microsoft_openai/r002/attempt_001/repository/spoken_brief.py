import os
from openai import OpenAI

from model_client import get_client


def generate_spoken_brief(payload, config=None):
    client = get_client(config)
    response = client.audio.speech.create(model='tts-1', input=payload['text'], voice='alloy')
    with open('spoken_brief.mp3', 'wb') as f:
        f.write(response.content)
    return {'file': 'spoken_brief.mp3'}