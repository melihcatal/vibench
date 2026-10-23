import os
from google.cloud import texttospeech
from speech_client import get_tts_client

def synthesize_ssml(ssml_text: str, voice_name: str, language_code: str = "en-US") -> bytes:
    """
    Synthesizes SSML with voice and prosody controls to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_tts_client()
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content