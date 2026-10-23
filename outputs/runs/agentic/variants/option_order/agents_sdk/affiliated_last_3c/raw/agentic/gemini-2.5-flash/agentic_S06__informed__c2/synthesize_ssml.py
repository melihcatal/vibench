from google.cloud import texttospeech
import os

def synthesize_ssml_text(ssml: str, voice_name: str = "en-US-Standard-A", language_code: str = "en-US", audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> bytes:
    """Synthesizes SSML text with voice and prosody controls using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content

