import os
import google.cloud.texttospeech as tts

# Credentials are picked up from environment variable GOOGLE_APPLICATION_CREDENTIALS
client = tts.TextToSpeechClient()


def synthesize_ssml(
    ssml: str, voice_name: str = None, audio_encoding: str = "MP3"
) -> bytes:
    """Synthesizes SSML with voice and prosody controls using Google Cloud Text‑to‑Speech.

    Args:
        ssml (str): SSML markup defining the narration.
        voice_name (str, optional): Specific voice name (e.g., "en-US-Wavenet-D").
        audio_encoding (str): Output format (MP3, LINEAR16, etc.).

    Returns:
        bytes: Synthesized speech as a byte stream.
    """
    input_ssml = tts.SynthesisInput(ssml=ssml)
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
