import os


def save_audio(audio_bytes: bytes, output_path: str) -> bool:
    """Write audio byte stream to a local file.

    Returns True on success, False otherwise.
    """
    try:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        return True
    except Exception as e:
        print(f"Failed to save audio: {e}")
        return False
