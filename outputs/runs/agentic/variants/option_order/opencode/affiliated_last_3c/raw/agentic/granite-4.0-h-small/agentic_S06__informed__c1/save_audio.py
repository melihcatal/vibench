import os


def save_audio_bytes(
    audio_bytes: bytes, output_path: str, format_hint: str = "mp3"
) -> None:
    """Writes raw audio bytes to a local file.

    Args:
        audio_bytes (bytes): The synthesized speech audio.
        output_path (str): Destination file path.
        format_hint (str): Optional hint for file extension (mp3, wav, etc.).
    """
    ext = format_hint.lower()
    if not output_path.endswith("." + ext):
        output_path += "." + ext
    with open(output_path, "wb") as f:
        f.write(audio_bytes)


def save_audio_file(content_obj: object, output_path: str):
    """Writes audio content from a provider response object to a local file.
    This generic helper works for any SDK where the audio is reachable as content_obj.audio_content.

    Args:
        content_obj: An object with an `audio_content` attribute (bytes).
        output_path (str): File path to write to.
    """
    audio_bytes = getattr(content_obj, "audio_content", None)
    if audio_bytes is None:
        raise ValueError("Provided object has no 'audio_content' attribute.")
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
