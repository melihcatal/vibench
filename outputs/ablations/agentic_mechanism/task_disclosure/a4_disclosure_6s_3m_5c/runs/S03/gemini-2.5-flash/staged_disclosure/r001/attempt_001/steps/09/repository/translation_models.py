
class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        if not isinstance(text, str) or not text:
            raise ValueError("Text must be a non-empty string.")
        if not isinstance(source_language, str) or not source_language:
            raise ValueError("Source language must be a non-empty string.")
        if not isinstance(target_language, str) or not target_language:
            raise ValueError("Target language must be a non-empty string.")

        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text: str):
        if not isinstance(translated_text, str):
            raise ValueError("Translated text must be a string.")
        self.translated_text = translated_text

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Input for normalization must be a string.")
    return text.strip()
