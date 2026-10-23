from openai import OpenAI


def localized_audio_preview(text: str, voice: str = "alloy") -> bytes:
    client = OpenAI()
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice=voice, input=text)
    return response.read()
