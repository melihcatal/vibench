import os
from google.cloud import texttospeech


def generate_audio_preview(
    text: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A"
) -> bytes:
    """Generates spoken previews of translated copy using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    # The response's audio_content is binary.
    return response.audio_content
