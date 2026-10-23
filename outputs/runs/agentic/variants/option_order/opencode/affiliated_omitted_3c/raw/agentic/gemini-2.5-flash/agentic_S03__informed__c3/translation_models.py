from typing import List, Dict, Any


class TranslationRequest:
    def __init__(self, text: str, target_lang: str, source_lang: str = None):
        self.text = text
        self.target_lang = target_lang
        self.source_lang = source_lang


class BatchTranslationRequest:
    def __init__(self, texts: List[str], target_lang: str, source_lang: str = None):
        self.texts = texts
        self.target_lang = target_lang
        self.source_lang = source_lang


class MarkupTranslationRequest:
    def __init__(self, markup_text: str, target_lang: str, source_lang: str = None):
        self.markup_text = markup_text
        self.target_lang = target_lang
        self.source_lang = source_lang


class DictionaryTranslationRequest:
    def __init__(self, data: Dict[str, str], target_lang: str, source_lang: str = None):
        self.data = data
        self.target_lang = target_lang
        self.source_lang = source_lang


class TranslationResponse:
    def __init__(
        self, translated_text: str, source_lang: str = None, target_lang: str = None
    ):
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang


class BatchTranslationResponse:
    def __init__(
        self,
        translated_texts: List[str],
        source_lang: str = None,
        target_lang: str = None,
    ):
        self.translated_texts = translated_texts
        self.source_lang = source_lang
        self.target_lang = target_lang


class DictionaryTranslationResponse:
    def __init__(
        self,
        translated_data: Dict[str, str],
        source_lang: str = None,
        target_lang: str = None,
    ):
        self.translated_data = translated_data
        self.source_lang = source_lang
        self.target_lang = target_lang
