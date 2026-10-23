class TranslationRequest:
    def __init__(self, text, source_language, target_language):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language


class TranslationResponse:
    def __init__(self, translated_text):
        self.translated_text = translated_text
