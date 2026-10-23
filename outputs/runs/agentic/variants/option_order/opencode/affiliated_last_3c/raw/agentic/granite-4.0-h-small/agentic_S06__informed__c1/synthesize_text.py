import os
import google.cloud.texttospeech as tts

# Credentials are picked up from environment variable GOOGLE_APPLICATION_CREDENTIALS
client = tts.TextToSpeechClient()


def synthesize_plain_text(
    text: str, voice_name: str = None, audio_encoding: str = "MP3"
) -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text‑to‑Speech.

    Args:
        text (str): The plain text to synthesize.
        voice_name (str, optional): Specific voice name (e.g., "en-US-Wavenet-D"). If None, the service defaults.
        audio_encoding (str): Desired audio encoding (MP3, LINEAR16, etc.).

    Returns:
        bytes: The synthesized speech as a byte stream.
    """
    input_ssml = tts.SynthesisInput(text=text)
    voice = (
        tts.VoiceSelectionParams(language_code="en-US", name=voice_name)
        if voice_name
        else None
    )
    audio_config = tts.AudioConfig(audio_encoding=audio_encoding)
    response = client.synthesize_speech(
        input=input_ssml, voice=voice, audio_config=audio_config
    )
    return response.audio_content
