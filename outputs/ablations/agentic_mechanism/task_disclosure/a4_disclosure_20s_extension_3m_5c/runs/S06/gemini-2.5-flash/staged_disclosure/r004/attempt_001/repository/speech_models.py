
class SynthesizeSpeechRequest:
    def __init__(self, text: str, voice_id: str, output_format: str):
        self.text = text
        self.voice_id = voice_id
        self.output_format = output_format

class SynthesizeSpeechResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content

def normalize_text_for_speech(text: str) -> str:
    # Placeholder for text normalization logic (e.g., expand abbreviations, numbers)
    return text

def validate_speech_request(request: SynthesizeSpeechRequest):
    if not request.text:
        raise ValueError("Text cannot be empty.")
    if not request.voice_id:
        raise ValueError("Voice ID cannot be empty.")
    if request.output_format not in ["mp3", "wav", "pcm"]: # Example formats
        raise ValueError(f"Unsupported output format: {request.output_format}")

