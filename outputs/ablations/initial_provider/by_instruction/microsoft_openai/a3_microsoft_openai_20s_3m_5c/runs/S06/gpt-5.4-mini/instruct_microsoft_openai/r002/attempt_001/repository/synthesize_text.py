from speech_client import client, default_tts_model
from speech_models import TextToSpeechRequest, TextToSpeechResult


def synthesize_text(text: str, voice: str | None = None, locale: str | None = None) -> TextToSpeechResult:
    req = TextToSpeechRequest(text=text, voice=voice, locale=locale)
    response = client().audio.speech.create(model=default_tts_model(), voice=req.voice or "alloy", input=req.text, response_format=req.output_format)
    return TextToSpeechResult(audio_bytes=response.read(), content_type="audio/mpeg", voice=req.voice or "alloy")
