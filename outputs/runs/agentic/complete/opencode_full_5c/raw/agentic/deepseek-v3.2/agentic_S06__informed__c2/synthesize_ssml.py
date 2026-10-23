import os
from google.cloud import texttospeech


def synthesize_ssml(
    ssml: str, language_code: str = "en-US", voice_name: str = "en-US-Neural2-F"
) -> bytes:
    """Synthesize SSML with voice and prosody controls using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
