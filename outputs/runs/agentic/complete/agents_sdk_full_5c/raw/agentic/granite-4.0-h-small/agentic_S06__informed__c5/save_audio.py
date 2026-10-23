import os
from speech_client import get_client

def save_audio(audio_bytes: bytes, file_path: str):
    """Write synthesized audio bytes to a local file.
    Handles directories creation if needed.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
    print(f"Audio saved to {file_path}")
