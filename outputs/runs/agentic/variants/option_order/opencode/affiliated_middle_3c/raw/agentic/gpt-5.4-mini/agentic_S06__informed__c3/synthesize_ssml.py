from speech_client import get_client
from speech_models import SpeechRequest, SpeechResponse


def synthesize_ssml(
    ssml: str, locale: str = "en-US", voice_name: str | None = None
) -> bytes:
    request = SpeechRequest(text=ssml, locale=locale, voice_name=voice_name)
    client = get_client()
    audio = client.text_to_speech.convert(
        text=request.normalized()["text"],
        voice_id=request.voice_name or "Rachel",
        model_id="eleven_multilingual_v2",
    )
    return audio if isinstance(audio, bytes) else bytes(audio)


def synthesize_ssml_response(
    ssml: str, locale: str = "en-US", voice_name: str | None = None
) -> SpeechResponse:
    audio = synthesize_ssml(ssml=ssml, locale=locale, voice_name=voice_name)
    return SpeechResponse(audio=audio, voice_name=voice_name)
