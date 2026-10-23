class DocumentRequest:
    def __init__(self, document_bytes):
        self.document_bytes = document_bytes

class DocumentResponse:
    def __init__(self, text):
        self.text = text

class TranslateRequest:
    def __init__(self, text, source_language, target_language):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class TranslateResponse:
    def __init__(self, translated_text):
        self.translated_text = translated_text

class ComprehendRequest:
    def __init__(self, text):
        self.text = text

class ComprehendResponse:
    def __init__(self, detected_sentiment):
        self.detected_sentiment = detected_sentiment