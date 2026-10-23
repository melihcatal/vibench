
class TranslationRequest:
    def __init__(self, text: str, target_language: str, source_language: str = "auto"):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language

class TranslationResponse:
    def __init__(self, translated_text: str, source_language: str, target_language: str):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

def normalize_text(text: str) -> str:
    """
    Normalizes text for translation by stripping leading/trailing whitespace
    and replacing multiple spaces with a single space.
    """
    return " ".join(text.strip().split())

def denormalize_text(text: str) -> str:
    """
    Denormalizes translated text if any specific normalization was applied
    that needs to be reversed. For now, it's a passthrough.
    """
    return text
