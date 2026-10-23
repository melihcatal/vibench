from speech_client import default_language_code, synthesize
from speech_models import SynthesisRequest


def synthesize_text(text: str, language_code: str | None = None, voice_name: str | None = None) -> bytes:
    request = SynthesisRequest(text=text, language_code=language_code or default_language_code(), voice_name=voice_name, ssml=False)
    return synthesize(request).audio_content
