# localized_audio_preview.py
import os
from gtts import gTTS

def generate_spoken_preview(text: str, lang: str = 'en', output_path: str = 'preview.mp3') -> str:
    """Create an audio file (MP3) with a spoken version of the translated text.
    Uses Google Text-to-Speech (gTTS) as a concrete provider.
    """
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    return output_path
