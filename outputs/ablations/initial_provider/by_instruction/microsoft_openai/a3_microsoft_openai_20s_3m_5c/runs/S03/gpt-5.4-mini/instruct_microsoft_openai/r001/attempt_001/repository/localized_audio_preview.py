from openai import OpenAI


def localized_audio_preview(text: str, voice: str = "alloy", language: str | None = None) -> bytes:
    client = OpenAI()
    audio = client.audio.speech.create(model="gpt-4o-mini-tts", voice=voice, input=text)
    return audio.read()
