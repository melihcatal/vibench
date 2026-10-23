from typing import Optional
import os
from google.cloud import texttospeech_v1 as texttospeech
from speech_client import get_speech_client
from speech_models import SynthesisInput, AudioConfig

def synthesize_ssml_to_audio(
    ssml: str,
    voice_name: str = "en-US-Studio-O",
    language_code: str = "en-US",
    audio_encoding: str = "MP3"
) -> bytes:
    """
    Synthesize SSML with voice and prosody controls using Google Cloud Text-to-Speech.
    """
    client = get_speech_client()
    
    input_data = SynthesisInput(ssml=ssml)
    voice_params = {
        "language_code": language_code,
        "name": voice_name
    }
    audio_config = AudioConfig(audio_encoding=audio_encoding)
    
    response = client.synthesize_speech(
        request={
            "input": input_data,
            "voice": voice_params,
            "audio_config": audio_config
        }
    )
    
    return response.audio_content