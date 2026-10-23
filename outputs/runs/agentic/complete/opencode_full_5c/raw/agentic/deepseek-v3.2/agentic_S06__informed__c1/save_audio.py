import os
from pathlib import Path


def save_audio_to_file(audio_bytes, output_path, format="mp3"):
    """Write synthesized speech audio to a local file."""
    output_path = Path(output_path)

    if format == "wav":
        if not output_path.suffix == ".wav":
            output_path = output_path.with_suffix(".wav")
    elif format == "mp3":
        if not output_path.suffix == ".mp3":
            output_path = output_path.with_suffix(".mp3")
    else:
        output_path = output_path.with_suffix(f".{format}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return str(output_path)


def save_audio_to_bytesio(audio_bytes):
    """Write synthesized speech audio to a BytesIO object."""
    from io import BytesIO

    audio_stream = BytesIO(audio_bytes)
    audio_stream.seek(0)
    return audio_stream
