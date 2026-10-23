import os
from speech_client import get_client

def synthesize_ssml(ssml: str, voice_name: str = None, output_path: str = None) -> bytes:
    """Synthesize SSML to audio bytes using Azure Speech TTS.
    Returns the raw audio bytes.
    If output_path is provided, the audio is also saved locally.
    """
    client = get_client()
    # Configure audio output format (MP3 22050Hz)
    audio_config = client.audio_config(format=client.AudioFormat.mp3, bitrate=32000, samplerate=22050)
    # SSML supports voice selection via <voice> tag; additional config optional
    result = client.synthesize_speech(text=ssml, voice_config=None, audio_config=audio_config)
    audio_bytes = result.audio_data
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes
