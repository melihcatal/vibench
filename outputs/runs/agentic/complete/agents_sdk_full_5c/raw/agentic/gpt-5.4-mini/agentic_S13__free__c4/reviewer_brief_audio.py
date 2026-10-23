from openai import OpenAI

from safety_client import get_openai_client


client: OpenAI = get_openai_client()
TTS_MODEL = "gpt-4o-mini-tts"
VOICE = "alloy"


def reviewer_brief_audio(brief_text: str):
    return client.audio.speech.create(model=TTS_MODEL, voice=VOICE, input=brief_text)
