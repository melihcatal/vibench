
class SpeechRequest:
    def __init__(self, text: str, voice_id: str):
        self.text = text
        self.voice_id = voice_id

class SpeechResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content

def normalize_text(text: str) -> str:
    # Basic normalization for text before sending to TTS
    return text.strip()
