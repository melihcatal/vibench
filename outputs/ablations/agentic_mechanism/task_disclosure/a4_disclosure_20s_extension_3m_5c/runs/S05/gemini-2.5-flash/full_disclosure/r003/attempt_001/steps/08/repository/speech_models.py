
class StreamingSpeechRequest:
    """
    Represents a streaming speech recognition request.
    """
    def __init__(self, audio_content: bytes = None, config: dict = None):
        self.audio_content = audio_content
        self.config = config

class RecognitionConfig:
    """
    Configuration for speech recognition.
    """
    def __init__(self, encoding: str = "LINEAR16", sample_rate_hertz: int = 16000,
                 language_code: str = "en-US", enable_automatic_punctuation: bool = False):
        self.encoding = encoding
        self.sample_rate_hertz = sample_rate_hertz
        self.language_code = language_code
        self.enable_automatic_punctuation = enable_automatic_punctuation

class StreamingRecognitionConfig:
    """
    Configuration for streaming speech recognition.
    """
    def __init__(self, config: RecognitionConfig, interim_results: bool = True):
        self.config = config
        self.interim_results = interim_results

class StreamingSpeechResponse:
    """
    Represents a streaming speech recognition response.
    """
    def __init__(self, results: list = None):
        self.results = results if results is not None else []

class SpeechRecognitionResult:
    """
    Represents a single speech recognition result.
    """
    def __init__(self, alternatives: list = None, is_final: bool = False):
        self.alternatives = alternatives if alternatives is not None else []
        self.is_final = is_final

class SpeechRecognitionAlternative:
    """
    Represents a single alternative hypothesis for a speech recognition result.
    """
    def __init__(self, transcript: str, confidence: float = 0.0):
        self.transcript = transcript
        self.confidence = confidence

def normalize_transcript(transcript: str) -> str:
    """
    Normalizes a transcript by performing basic cleaning.
    """
    return transcript.strip().lower()

