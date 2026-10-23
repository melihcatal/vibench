
class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

    def to_dict(self):
        return {
            "text": self.text,
            "source_language": self.source_language,
            "target_language": self.target_language
        }

class TranslationResponse:
    def __init__(self, translated_text: str, detected_language: str = None):
        self.translated_text = translated_text
        self.detected_language = detected_language

    def to_dict(self):
        return {
            "translated_text": self.translated_text,
            "detected_language": self.detected_language
        }

def normalize_text(text: str) -> str:
    """
    Performs basic normalization on text, e.g., stripping whitespace.
    Further normalization logic can be added here as needed.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    return text.strip()

