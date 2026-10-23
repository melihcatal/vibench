from speech_client import default_language_code, synthesize
from speech_models import SynthesisRequest


def synthesize_ssml(ssml: str, language_code: str | None = None, voice_name: str | None = None, speaking_rate: float = 1.0, pitch: float = 0.0) -> bytes:
    request = SynthesisRequest(text=ssml, language_code=language_code or default_language_code(), voice_name=voice_name, speaking_rate=speaking_rate, pitch=pitch, ssml=True)
    return synthesize(request).audio_content
