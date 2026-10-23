from speech_client import get_tts_client
from speech_models import build_synthesis_request
from typing import Optional


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: Optional[str] = None,
) -> bytes:
    client = get_tts_client()
    synthesis_input, voice, audio_config = build_synthesis_request(
        ssml=ssml,
        language_code=language_code,
        voice_name=voice_name,
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
