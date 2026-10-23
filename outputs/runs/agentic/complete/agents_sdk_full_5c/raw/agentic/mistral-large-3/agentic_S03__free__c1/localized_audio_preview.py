import os
from typing import Optional
from google.cloud import texttospeech_v1

def localized_audio_preview(
    text: str,
    language_code: str,
    voice_name: Optional[str] = None,
    output_format: str = "MP3",
) -> bytes:
    """Generate spoken previews of translated copy using Google Cloud Text-to-Speech API."""
    client = texttospeech_v1.TextToSpeechClient()
    
    voice = voice_name or f"{language_code}-Standard-A"
    input_text = texttospeech_v1.SynthesisInput(text=text)
    voice_params = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code, name=voice
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=getattr(texttospeech_v1.AudioEncoding, output_format)
    )
    
    response = client.synthesize_speech(
        input=input_text, voice=voice_params, audio_config=audio_config
    )
    
    return response.audio_content