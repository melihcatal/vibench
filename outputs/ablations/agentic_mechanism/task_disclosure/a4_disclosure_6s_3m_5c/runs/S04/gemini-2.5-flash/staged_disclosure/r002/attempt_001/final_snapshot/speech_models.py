
class SpeechRecognitionRequest:
    def __init__(self, audio_uri: str, language_code: str):
        self.audio_uri = audio_uri
        self.language_code = language_code

class SpeechRecognitionResponse:
    def __init__(self, transcript: str, confidence: float):
        self.transcript = transcript
        self.confidence = confidence

def normalize_transcript(transcript: str) -> str:
    """
    Normalizes the transcript by performing basic cleaning.
    """
    return transcript.strip().lower()

