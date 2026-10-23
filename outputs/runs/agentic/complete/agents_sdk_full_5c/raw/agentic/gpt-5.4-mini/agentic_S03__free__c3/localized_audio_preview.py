import base64

from openai import OpenAI

PROVIDER = "openai:tts-1"


def generate_spoken_preview(text: str, voice: str = "alloy") -> dict:
    client = OpenAI()
    audio = client.audio.speech.create(model="tts-1", voice=voice, input=text)
    data = audio.read() if hasattr(audio, "read") else b""
    return {"audio_base64": base64.b64encode(data).decode("utf-8"), "provider": PROVIDER}
