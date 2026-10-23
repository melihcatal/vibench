from speech_client import openai_client, preferred_voice
from speech_models import SpeechRequest, SpeechResponse, normalize_text


def synthesize_text(text: str, locale: str = "en-US", voice: str = None, model: str = None) -> SpeechResponse:
    client = openai_client()
    request = SpeechRequest(text=normalize_text(text), locale=locale, voice=voice or preferred_voice(locale), format="mp3")
    response = client.audio.speech.create(
        model=model or "gpt-4o-mini-tts",
        voice=request.voice,
        input=request.text,
        response_format="mp3",
    )
    return SpeechResponse(audio_bytes=response.read(), content_type="audio/mpeg", meta={"model": model or "gpt-4o-mini-tts", "voice": request.voice})
