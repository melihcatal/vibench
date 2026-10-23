import os
from typing import Dict, Any
from google.cloud import texttospeech
from translation_client import get_project_id # Re-using for project ID
from translation_models import LocalizedAudioPreviewRequest, LocalizedAudioPreviewResponse

def generate_localized_audio_preview(payload: LocalizedAudioPreviewRequest, config: Dict[str, Any] = None) -> LocalizedAudioPreviewResponse:
    config = config or {}
    project_id = config.get("project_id", get_project_id())
    
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=payload.text)

    # Select the language and SSML voice type
    # The voice_name can be specified, otherwise Google Cloud Text-to-Speech will choose a default for the language.
    voice = texttospeech.VoiceSelectionParams(
        language_code=payload.language,
        name=payload.voice_name if payload.voice_name else None # Use specific voice if provided
    )

    # Select the type of audio file you want returned
    audio_encoding_map = {
        "MP3": texttospeech.AudioEncoding.MP3,
        "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
        "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
    }
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding_map.get(payload.audio_encoding, texttospeech.AudioEncoding.MP3)
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return LocalizedAudioPreviewResponse(
        audio_content=response.audio_content,
        audio_encoding=payload.audio_encoding
    )
