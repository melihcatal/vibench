
class SpeechRequest:
    def __init__(self, text: str, voice: str = "default", speed: float = 1.0):
        self.text = text
        self.voice = voice
        self.speed = speed

class SpeechResponse:
    def __init__(self, audio_content: bytes, audio_format: str = "mp3"):
        self.audio_content = audio_content
        self.audio_format = audio_format

def normalize_text(text: str) -> str:
    """
    Normalizes the input text for Text-to-Speech synthesis.
    This can include cleaning, expanding abbreviations, or other pre-processing steps.
    """
    # Example normalization: trim whitespace
    return text.strip()
