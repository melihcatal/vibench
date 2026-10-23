import os
from gtts import gTTS  # pip install gtts

def generate_audio_brief(brief_text: str, output_path: str = 'moderation_brief.mp3') -> str:
    """Create a spoken brief for a moderation reviewer using Google Text-to-Speech.

    Uses the gtts library which calls the public Google Cloud Text-to-Speech API.
    """
    tts = gTTS(text=brief_text, lang='en')
    tts.save(output_path)
    return output_path
