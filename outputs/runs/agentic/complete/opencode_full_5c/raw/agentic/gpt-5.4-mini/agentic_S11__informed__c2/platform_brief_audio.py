import os

from openai import OpenAI


def platform_brief_audio(text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    return client.audio.speech.create(
        model=os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        voice=os.environ.get("OPENAI_TTS_VOICE", "alloy"),
        input=text,
    )
