import os
from openai import OpenAI


def generate_spoken_brief(text, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.speech.create(model='tts-1', text=text, voice='alloy')
    return {'audio_url': response.url}