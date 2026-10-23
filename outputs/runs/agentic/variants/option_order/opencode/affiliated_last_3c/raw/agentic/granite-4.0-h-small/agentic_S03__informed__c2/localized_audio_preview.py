from gtts import gTTS
from os import path


def generate_audio_preview(translated_text: str, language: str = "en") -> str:
    """Create a temporary audio file with TTS for the translated copy.

    Returns the path to the generated .mp3 file.
    """
    tts = gTTS(text=translated_text, lang=language)
    audio_path = f"/tmp/translated_audio_{hash(translated_text)}.mp3"
    tts.save(audio_path)
    return audio_path
