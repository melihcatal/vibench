from typing import List, Dict

class TranslationRequest:
    def __init__(self, source_language: str, target_language: str, content: str):
        self.source_language = source_language
        self.target_language = target_language
        self.content = content

class TranslationResponse:
    def __init__(self, translated_content: str):
        self.translated_content = translated_content

class TranslationNormalizer:
    @staticmethod
    def normalize(response: Dict) -> str:
        return response['translations'][0]['content']