import os

def save_audio(audio_bytes, output_path):
    """Write raw audio bytes (e.g., LINEAR16) to a local file.
    Args:
        audio_bytes (bytes): Audio data returned from TTS service.
        output_path (str): Destination file path (e.g., 'output.wav').
    """
    with open(output_path, 'wb') as f:
        f.write(audio_bytes)
    print(f"Audio saved to {output_path}")
