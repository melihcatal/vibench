import os

def save_audio_to_file(audio_content: bytes, filename: str):
    """Writes synthesized speech audio to a local file."""
    try:
        with open(filename, "wb") as out:
            out.write(audio_content)
        print(f"Audio content written to file '{filename}'")
    except Exception as e:
        print(f"Error saving audio to file: {e}")

