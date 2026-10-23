import os
from google.cloud import texttospeech


def synthesize_text(
    text: str, voice_name: str = "en-US-Wavenet-D", audio_encoding: str = "MP3"
) -> bytes:
    """Synthesize plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text (str): The plain text to synthesize.
        voice_name (str): Voice name to use (default: 'en-US-Wavenet-D').
        audio_encoding (str): Audio encoding (default: 'MP3').

    Returns:
        bytes: The synthesized speech as a byte stream.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "path/to/credentials.json"
    )
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    return response.audio_content
