import os
from speech_client import get_client

def synthesize(text: str, voice_name: str = None, output_path: str = None) -> bytes:
    """Synthesize plain text to audio bytes using Azure Speech TTS.
    Returns the raw audio bytes.
    If output_path is provided, the audio is also saved locally.
    """
    client = get_client()
    # Configure audio output format (e.g., MP3 22050Hz)
    audio_config = client.audio_config(format=client.AudioFormat.mp3, bitrate=32000, samplerate=22050)
    # Choose voice if provided, else default
    if voice_name:
        voice_config = client.VoiceConfiguration(name=voice_name)
    else:
        voice_config = None
    result = client.synthesize_speech(text=text, voice_config=voice_config, audio_config=audio_config)
    audio_bytes = result.audio_data
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes
