# This file defines local request, response, and normalization helpers.
# For simplicity, we'll use basic dictionaries or simple classes here
# rather than a full Pydantic setup, as not explicitly required.

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

class SummarizationRequest:
    def __init__(self, document_content: str):
        self.document_content = document_content

class EmbeddingRequest:
    def __init__(self, text_segment: str):
        self.text_segment = text_segment

class AudioPreviewRequest:
    def __init__(self, text: str, language_code: str, voice_name: str = "en-US-Standard-A"):
        self.text = text
        self.language_code = language_code
        self.voice_name = voice_name
