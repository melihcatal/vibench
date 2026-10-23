import os

from speech_client import openai_client, preferred_voice
from speech_models import SpeechResponse, normalize_text


def synthesize_ssml(ssml: str, locale: str = "en-US", voice: str = None, model: str = None) -> SpeechResponse:
    client = openai_client()
    selected_voice = voice or preferred_voice(locale)
    prompt = normalize_text(ssml)
    response = client.audio.speech.create(
        model=model or os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        voice=selected_voice,
        input=prompt,
        response_format="mp3",
    )
    return SpeechResponse(audio_bytes=response.read(), content_type="audio/mpeg", meta={"voice": selected_voice, "ssml": True})
