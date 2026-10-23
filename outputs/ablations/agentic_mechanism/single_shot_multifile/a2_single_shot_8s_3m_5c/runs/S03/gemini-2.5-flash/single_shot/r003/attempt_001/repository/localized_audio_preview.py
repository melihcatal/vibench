import os
from typing import Optional
from google.cloud import texttospeech_v1 as texttospeech
from translation_models import AudioPreviewResult

def generate_audio_preview(
    text: str,
    language_code: str,
    voice_name: Optional[str] = None,
    audio_encoding: str = "MP3",
) -> AudioPreviewResult:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice_selection = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding),
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection,
        audio_config=audio_config,
    )

    return AudioPreviewResult(
        audio_content_bytes=response.audio_content,
        audio_encoding=audio_encoding,
    )
