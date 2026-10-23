# save_audio.py
import os
from pathlib import Path


def save_audio(audio_bytes, output_path):
    """Write synthesized audio bytes to a local file. If output_path ends with .mp3 it preserves
    the MP3 encoding; otherwise it writes raw PCM.","""
    Path(output_path).write_bytes(audio_bytes)
    print(f"Audio saved to {output_path}")
