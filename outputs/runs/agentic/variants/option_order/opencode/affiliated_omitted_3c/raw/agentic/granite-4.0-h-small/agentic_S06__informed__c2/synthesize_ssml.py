import os

from speech_client import TextToSpeechClient


def synthesize_ssml(
    ssml: str,
    voice_name: str = None,
    prosody_pitch: float = 0.0,
    prosody_rate: float = 1.0,
) -> bytes:
    """Synthesize SSML with optional voice, pitch, and rate adjustments.

    Args:
        ssml (str): SSML string to synthesize.
        voice_name (str, optional): Voice identifier for the provider.
        prosody_pitch (float, optional): Pitch adjustment (e.g., 1.2 = +20%).
        prosody_rate (float, optional): Speaking rate relative to default (e.g., 1.0 = normal).

    Returns:
        bytes: Audio byte stream from the TTS service.
    """
    client = TextToSpeechClient()
    response = client.synthesize_speech(
        input_ssml=ssml,
        voice_name=voice_name,
        prosody_pitch=prosody_pitch,
        prosody_rate=prosody_rate,
    )
    return response.audio_bytes
