import os
from typing import Dict, Any
from google.cloud import texttospeech_v1 as texttospeech

def generate_audio_brief(text: str, language_code: str = "en-US") -> Dict[str, Any]:
    """
    Generates spoken briefings from Cohere model outputs using Google Cloud Text-to-Speech API.
    Returns audio content in base64 and synthesis metadata.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return {
        "audio_content": response.audio_content,
        "audio_encoding": "MP3",
        "language_code": language_code,
    }