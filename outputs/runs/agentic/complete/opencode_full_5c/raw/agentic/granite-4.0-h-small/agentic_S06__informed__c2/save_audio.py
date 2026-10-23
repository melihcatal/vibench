# [SAME-SCENARIO] save_audio.py
# Writes synthesized speech audio to a local file or object storage
# Uses ElevenLabs SDK to upload the audio bytes

import os
from elevenlabs import ElevenLabs, AudioFormat

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize SDK client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def save_audio(audio_bytes: bytes, file_path: str):
    """Save raw audio bytes to a local file.

    Args:
        audio_bytes (bytes): The synthesized audio data.
        file_path (str): Destination file path (e.g., /tmp/output.wav).
    """
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
    print(f"Audio saved to {file_path}")


# Example usage (requires API key in env)
if __name__ == "__main__":
    # Assuming audio_bytes is obtained from previous synthesis step
    sample_path = "/tmp/demo.wav"
    # Placeholder: replace with actual audio bytes fetched from synthesis call
    audio_bytes = b"placeholder"
    save_audio(audio_bytes, sample_path)
