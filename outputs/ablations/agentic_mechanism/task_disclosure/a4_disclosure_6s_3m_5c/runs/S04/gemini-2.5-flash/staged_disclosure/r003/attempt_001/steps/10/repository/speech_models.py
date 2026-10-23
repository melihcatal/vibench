
class SpeechContext:
    def __init__(self, phrases: list[str] = None, boost: float = None):
        self.phrases = phrases if phrases is not None else []
        self.boost = boost

class RecognitionConfig:
    def __init__(self,
                 encoding: str = None,
                 sample_rate_hertz: int = None,
                 language_code: str = None,
                 max_alternatives: int = 1,
                 profanity_filter: bool = False,
                 speech_contexts: list[SpeechContext] = None,
                 enable_word_time_offsets: bool = False):
        self.encoding = encoding
        self.sample_rate_hertz = sample_rate_hertz
        self.language_code = language_code
        self.max_alternatives = max_alternatives
        self.profanity_filter = profanity_filter
        self.speech_contexts = speech_contexts if speech_contexts is not None else []
        self.enable_word_time_offsets = enable_word_time_offsets

class RecognitionAudio:
    def __init__(self, uri: str = None, content: bytes = None):
        self.uri = uri
        self.content = content

class RecognizeRequest:
    def __init__(self, config: RecognitionConfig, audio: RecognitionAudio):
        self.config = config
        self.audio = audio

class WordInfo:
    def __init__(self, start_time: str, end_time: str, word: str):
        self.start_time = start_time
        self.end_time = end_time
        self.word = word

class SpeechRecognitionAlternative:
    def __init__(self, transcript: str, confidence: float, words: list[WordInfo] = None):
        self.transcript = transcript
        self.confidence = confidence
        self.words = words if words is not None else []

class SpeechRecognitionResult:
    def __init__(self, alternatives: list[SpeechRecognitionAlternative]):
        self.alternatives = alternatives

class RecognizeResponse:
    def __init__(self, results: list[SpeechRecognitionResult]):
        self.results = results

def normalize_transcript(response: RecognizeResponse) -> str:
    """
    Normalizes the transcript from a speech recognition response.
    This is a basic example; more complex normalization might involve
    punctuation, casing, and number formatting.
    """
    if not response or not response.results:
        return ""

    normalized_text = []
    for result in response.results:
        if result.alternatives:
            # Take the most confident alternative
            normalized_text.append(result.alternatives[0].transcript)
    return " ".join(normalized_text)

