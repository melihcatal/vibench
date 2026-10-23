class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text: str, detected_language: str = None):
        self.translated_text = translated_text
        self.detected_language = detected_language

def normalize_text(text: str) -> str:
    # Example normalization: strip whitespace and convert to lowercase
    return text.strip().lower()
