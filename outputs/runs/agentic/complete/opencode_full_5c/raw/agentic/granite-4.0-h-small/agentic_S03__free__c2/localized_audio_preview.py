# localized_audio_preview.py
import os
import tempfile
import subprocess
from gtts import gTTS  # pip install gTTS

# Simple helper to generate an audio preview from translated text using Google Text‑to‑Speech.


def generate_audio_preview(translated_text: str, language: str = "en") -> str:
    """Create an MP3 file with spoken audio of the translated text."""
    tts = gTTS(text=translated_text, lang=language)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(tts.read())
        audio_path = tmp.name
    return audio_path


if __name__ == "__main__":
    preview = generate_audio_preview("Hello world!", language="es")
    print("Audio preview written to:", preview)
