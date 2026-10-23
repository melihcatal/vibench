import os
import wave
import contextlib
from typing import Union

def save_audio_bytes(audio_bytes: bytes, output_path: str, format: str = "mp3") -> None:
    """Write raw audio bytes to a local file.

    Args:
        audio_bytes (bytes): The audio data retrieved from a TTS API.
        output_path (str): Destination file path (including extension).
        format (str): Optional; if provided, may adjust container handling (ignored for raw bytes).
    """
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

# Optional helper to save as WAV if raw PCM is received
# This example assumes 16‑bit little‑endian PCM

def save_pcm_to_wav(pcm_bytes: bytes, output_path: str, sample_rate: int = 24000) -> None:
    with open(output_path, "wb") as f:
        with contextlib.closing(wave.open(f, "wb")) as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm_bytes)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     # assume `audio` is the bytes returned from a TTS call
#     save_audio_bytes(audio, "output.wav", format="wav")
