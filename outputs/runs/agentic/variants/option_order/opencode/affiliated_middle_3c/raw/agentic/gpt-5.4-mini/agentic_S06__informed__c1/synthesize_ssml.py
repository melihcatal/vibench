from speech_client import synthesize_request
from speech_models import SpeechRequest


def synthesize_ssml(
    ssml: str,
    voice_name: str = None,
    language_code: str = None,
    speaking_rate: float = None,
    pitch: float = None,
) -> bytes:
    response = synthesize_request(
        SpeechRequest(
            text=ssml,
            voice_name=voice_name,
            language_code=language_code,
            ssml=True,
            speaking_rate=speaking_rate,
            pitch=pitch,
        )
    )
    return response.audio_bytes
