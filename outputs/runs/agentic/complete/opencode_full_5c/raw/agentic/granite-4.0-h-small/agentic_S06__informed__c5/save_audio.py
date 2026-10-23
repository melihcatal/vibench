import os
import pathlib
import io


def save_audio_bytes(audio_bytes: bytes, output_path: str):
    """Write raw audio bytes to a local file.

    Args:
        audio_bytes (bytes): Binary audio data.
        output_path (str): Destination file path (including extension .wav/.mp3).
    """
    pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)


def save_audio_stream(audio_stream: io.BytesIO, output_path: str):
    """Save audio from an in‑memory BytesIO stream to a file.

    Args:
        audio_stream (io.BytesIO): Stream containing audio bytes.
        output_path (str): Destination file path.
    """
    save_audio_bytes(audio_stream.getvalue(), output_path)
