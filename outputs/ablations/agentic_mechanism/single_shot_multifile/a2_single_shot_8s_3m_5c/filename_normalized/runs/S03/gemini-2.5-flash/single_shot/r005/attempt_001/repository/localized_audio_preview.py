import os
import base64
from typing import Dict, Any
from translation_client import get_google_tts_client
from translation_models import create_audio_preview_result
from google.cloud import texttospeech_v1

def generate_audio_preview(
    text: str,
    language_code: str,
    voice_name: str = "en-US-Standard-A"
) -> Dict[str, Any]:
    client = get_google_tts_client()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config
        }
    )

    audio_content_base64 = base64.b64encode(response.audio_content).decode('utf-8')
    
    return create_audio_preview_result(text=text, audio_content_base64=audio_content_base64, language_code=language_code)
