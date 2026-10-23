class SpeechRecognitionResult:
    def __init__(self, text: str, confidence: float = 0.0, is_final: bool = False):
        self.text = text
        self.confidence = confidence
        self.is_final = is_final

    def __repr__(self):
        return f"SpeechRecognitionResult(text='{self.text}', confidence={self.confidence}, is_final={self.is_final})"

class StreamingRecognitionConfig:
    def __init__(self, language: str = "en-US", enable_punctuation: bool = True):
        self.language = language
        self.enable_punctuation = enable_punctuation
