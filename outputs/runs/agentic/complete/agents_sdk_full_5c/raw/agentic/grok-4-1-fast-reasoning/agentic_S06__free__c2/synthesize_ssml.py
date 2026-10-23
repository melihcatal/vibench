import os
from typing import Optional
from speech_client import get_tts_client
from speech_models import build_synthesis_input, build_voice_params, build_audio_config

def synthesize_ssml(
    ssml: str,
    voice_name: str = "en-US-Standard-A",
    language_code: str = "en-US"
) -> bytes:
    client = get_tts_client()
    input_ = build_synthesis_input(ssml=ssml)
    voice = build_voice_params(language_code=language_code, name=voice_name)
    audio_config = build_audio_config()
    response = client.synthesize_speech(
        input=input_,
        voice=voice,
        audio_config=audio_config
    )
    return response.audio_content
