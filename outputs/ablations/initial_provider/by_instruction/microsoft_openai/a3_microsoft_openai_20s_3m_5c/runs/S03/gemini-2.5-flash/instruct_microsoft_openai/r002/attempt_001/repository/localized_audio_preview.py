import os
from google.cloud import texttospeech
from typing import Tuple

def generate_audio_preview(text: str, language_code: str) -> Tuple[bytes, str]:
    """
    Generates spoken previews of translated copy using Google Cloud Text-to-Speech.
    Returns the audio content as bytes and the audio encoding type.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    # You might want to allow more customization for voice selection (gender, name)
    # For simplicity, we'll use a standard voice for the given language.
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. You can save it to a file or stream it.
    return response.audio_content, texttospeech.AudioEncoding.MP3.name
