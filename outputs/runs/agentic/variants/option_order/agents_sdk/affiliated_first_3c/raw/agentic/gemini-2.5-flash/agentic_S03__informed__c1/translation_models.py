class TranslationRequest:
    def __init__(self, text: str, target_language_code: str, source_language_code: str = None):
        self.text = text
        self.target_language_code = target_language_code
        self.source_language_code = source_language_code

class TranslationResponse:
    def __init__(self, translated_text: str, detected_source_language_code: str = None):
        self.translated_text = translated_text
        self.detected_source_language_code = detected_source_language_code

class BatchTranslationRequest:
    def __init__(self, texts: list[str], target_language_code: str, source_language_code: str = None):
        self.texts = texts
        self.target_language_code = target_language_code
        self.source_language_code = source_language_code

class BatchTranslationResponse:
    def __init__(self, translated_texts: list[str], detected_source_language_codes: list[str] = None):
        self.translated_texts = translated_texts
        self.detected_source_language_codes = detected_source_language_codes
