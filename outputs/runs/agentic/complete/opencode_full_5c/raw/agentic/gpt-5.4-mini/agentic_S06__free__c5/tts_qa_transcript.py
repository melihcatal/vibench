import os

from openai import OpenAI


def tts_qa_transcript(audio_bytes: bytes, language: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=("sample.wav", audio_bytes), language=language)
    return response.text
