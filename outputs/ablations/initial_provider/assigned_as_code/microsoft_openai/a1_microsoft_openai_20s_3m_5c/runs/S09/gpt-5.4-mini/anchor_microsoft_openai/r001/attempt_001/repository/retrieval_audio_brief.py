import os

from openai import OpenAI


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    brief = payload['brief']
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.audio.speech.create(model='gpt-4o-mini-tts', voice='alloy', input=brief)
    return {'audio': response.read()}
