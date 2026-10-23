import os
import gtts
from model_models import normalize_chat_response

def spoken_brief(model_output: str, language: str = "en") -> None:
    """Generate a spoken (audio) brief from model output using Google Text-to-Speech.

    Saves file named brief.mp3 in the current directory.
    """
    tts = gtts.gTTS(text=model_output, lang=language)
    tts.save("brief.mp3")
    print("Audio brief saved as brief.mp3")

if __name__ == "__main__":
    brief_text = "This is a short spoken summary of the latest model response."
    spoken_brief(brief_text)
