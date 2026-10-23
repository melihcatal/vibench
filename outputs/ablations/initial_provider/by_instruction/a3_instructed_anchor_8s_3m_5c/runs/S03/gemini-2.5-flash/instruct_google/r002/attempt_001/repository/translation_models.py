class TranslationRequest:
    def __init__(self, text, target_language, source_language=None):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language

class TranslationResponse:
    def __init__(self, translated_text, detected_source_language=None):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language
