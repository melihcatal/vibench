from __future__ import annotations

import os
from openai import OpenAI

PROVIDER_NAME = 'OpenAI'
TTS_MODEL = 'gpt-4o-mini-tts'
VOICE = 'alloy'


def generate_audio_preview(text: str) -> bytes:
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.audio.speech.create(model=TTS_MODEL, voice=VOICE, input=text)
    return response.read()
