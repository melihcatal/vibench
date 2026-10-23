class TranslationRequest:
    def __init__(self, text, target_language):
        self.text = text
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text):
        self.translated_text = translated_text