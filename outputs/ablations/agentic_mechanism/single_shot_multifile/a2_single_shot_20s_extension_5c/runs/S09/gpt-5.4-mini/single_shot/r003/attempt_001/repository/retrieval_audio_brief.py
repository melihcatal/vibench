import os
from typing import List

from openai import OpenAI

MODEL_ID = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")
VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


def retrieval_audio_brief(search_results: List[str]) -> bytes:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL") or None)
    text = "Provide a short spoken brief summarizing these retrieved results:\n" + "\n".join(search_results[:10])
    audio = client.audio.speech.create(model=MODEL_ID, voice=VOICE, input=text)
    return audio.read()
