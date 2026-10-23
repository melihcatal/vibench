import os

def save_audio(audio_bytes: bytes, output_path: str, format: str = "wav") -> None:
    """Write the audio byte stream to a local file.
    format: currently only 'wav' is supported; additional formats can be added later.
    """
    if format.lower() != "wav":
        raise NotImplementedError(f"Format '{format}' not supported")
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
