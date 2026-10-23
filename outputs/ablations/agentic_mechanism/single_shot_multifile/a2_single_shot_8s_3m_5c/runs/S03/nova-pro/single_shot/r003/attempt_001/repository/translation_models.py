class TranslationRequest:
    def __init__(self, text, target_language):
        self.text = text
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text, detected_source_language):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language

def normalize_response(response):
    return TranslationResponse(response['translatedText'], response['detectedSourceLanguage']) if response else None
