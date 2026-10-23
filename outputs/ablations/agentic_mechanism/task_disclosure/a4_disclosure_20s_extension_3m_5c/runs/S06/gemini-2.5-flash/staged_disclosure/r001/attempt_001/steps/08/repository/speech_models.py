
class TTSRequest:
    def __init__(self, text: str, voice_id: str = "default", speed: float = 1.0):
        self.text = text
        self.voice_id = voice_id
        self.speed = speed

class TTSResponse:
    def __init__(self, audio_content: bytes, audio_format: str = "mp3"):
        self.audio_content = audio_content
        self.audio_format = audio_format

def normalize_text(text: str) -> str:
    """
    Normalizes the input text for Text-to-Speech processing.
    This can include cleaning, expanding abbreviations, etc.
    """
    # Example normalization: strip leading/trailing whitespace and replace multiple spaces
    normalized = ' '.join(text.strip().split())
    return normalized

def create_tts_request(text: str, voice: str = "default", speed: float = 1.0) -> TTSRequest:
    """
    Helper function to create a TTSRequest object.
    """
    return TTSRequest(text=normalize_text(text), voice_id=voice, speed=speed)

def process_tts_response(audio_data: bytes, format: str = "mp3") -> TTSResponse:
    """
    Helper function to process raw audio data into a TTSResponse object.
    """
    return TTSResponse(audio_content=audio_data, audio_format=format)
