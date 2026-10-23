class TranslationRequest:
    def __init__(self, text, source_language, target_language):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class BatchTranslationRequest:
    def __init__(self, texts, source_language, target_language):
        self.texts = texts
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, text, source_language, target_language):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class BatchTranslationResponse:
    def __init__(self, translations, source_language, target_language):
        self.translations = translations
        self.source_language = source_language
        self.target_language = target_language
