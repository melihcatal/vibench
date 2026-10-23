import os
from openai import OpenAI

def reviewer_brief_audio(brief: str) -> bytes:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=brief
    )
    return speech_response.content
