
class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text: str, source_language: str, target_language: str):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language

def normalize_translation_response(response: TranslationResponse) -> str:
    """
    Normalizes the translation response.
    This is a placeholder function; actual normalization logic would depend on the specific translation service.
    """
    return response.translated_text
