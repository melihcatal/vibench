import os
def save_audio(audio_bytes: bytes, output_path: str, format_hint: str = "mp3") -> None:
    """Write synthesized speech audio bytes to a local file.

    In a production setting this could also store to an object storage bucket.
    """
    if not output_path.endswith(f".{format_hint}"):
        output_path += f".{format_hint}"
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    print(f"Audio saved to {output_path}")