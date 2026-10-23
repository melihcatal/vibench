
class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

def normalize_translation_response(raw_response: dict) -> TranslationResponse:
    # This is a placeholder for actual normalization logic.
    # Assumes raw_response is a dictionary with a 'translatedText' key.
    translated_text = raw_response.get('translatedText', '')
    return TranslationResponse(translated_text)
