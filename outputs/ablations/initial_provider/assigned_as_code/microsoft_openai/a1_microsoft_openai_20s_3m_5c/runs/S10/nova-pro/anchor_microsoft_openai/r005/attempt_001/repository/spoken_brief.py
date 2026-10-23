import os
from openai import OpenAI

def generate_spoken_brief(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.audio.speech.create(model='tts-1',
            input=payload['text'])
    return {'audio': response.content}
