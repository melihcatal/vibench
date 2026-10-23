from speech_client import synthesize_request
from speech_models import SpeechRequest


def synthesize_text(
    text: str, voice_name: str = None, language_code: str = None
) -> bytes:
    response = synthesize_request(
        SpeechRequest(
            text=text, voice_name=voice_name, language_code=language_code, ssml=False
        )
    )
    return response.audio_bytes
