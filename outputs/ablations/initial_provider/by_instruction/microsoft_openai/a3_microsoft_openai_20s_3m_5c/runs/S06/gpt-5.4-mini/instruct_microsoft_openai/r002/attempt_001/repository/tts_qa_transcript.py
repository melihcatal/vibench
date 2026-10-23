from openai import OpenAI

from speech_client import client, default_transcribe_model


def transcribe_audio(audio_bytes: bytes) -> str:
    c: OpenAI = client()
    response = c.audio.transcriptions.create(model=default_transcribe_model(), file=("sample.wav", audio_bytes))
    return response.text
