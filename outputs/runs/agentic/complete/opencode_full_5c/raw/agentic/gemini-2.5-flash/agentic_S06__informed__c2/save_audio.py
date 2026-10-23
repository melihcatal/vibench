import os


def save_audio_to_file(audio_content: bytes, filename: str):
    """Writes synthesized speech audio bytes to a local file.

    This utility is designed to save the audio output from a Text-to-Speech (TTS) service.
    """
    try:
        with open(filename, "wb") as out:
            out.write(audio_content)
        print(f"Audio content written to file: {filename}")
    except IOError as e:
        print(f"Error writing audio to file {filename}: {e}")


def save_audio_to_object(audio_content: bytes) -> bytes:
    """Returns synthesized speech audio bytes directly for in-memory object storage.

    This utility is designed to handle the audio output from a Text-to-Speech (TTS) service.
    """
    return audio_content
