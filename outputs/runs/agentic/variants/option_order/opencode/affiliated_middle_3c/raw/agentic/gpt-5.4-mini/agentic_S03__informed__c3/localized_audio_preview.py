from openai import OpenAI

from translation_models import normalize_text


def localized_audio_preview(text: str) -> bytes:
    client = OpenAI()
    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=normalize_text(text)
    )
    return audio.read()
