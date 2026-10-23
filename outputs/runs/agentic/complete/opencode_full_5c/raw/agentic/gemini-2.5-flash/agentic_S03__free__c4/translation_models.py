from typing import List, Dict, Any


class TranslationRequest:
    def __init__(
        self,
        texts: List[str],
        target_language_code: str,
        source_language_code: str = "",
    ):
        self.texts = texts
        self.target_language_code = target_language_code
        self.source_language_code = source_language_code


class TranslationResponse:
    def __init__(self, translated_texts: List[str], original_texts: List[str] = None):
        self.translated_texts = translated_texts
        self.original_texts = original_texts if original_texts is not None else []


class DictionaryTranslationRequest:
    def __init__(
        self,
        dictionary: Dict[str, str],
        target_language_code: str,
        source_language_code: str = "",
    ):
        self.dictionary = dictionary
        self.target_language_code = target_language_code
        self.source_language_code = source_language_code


class DictionaryTranslationResponse:
    def __init__(self, translated_dictionary: Dict[str, str]):
        self.translated_dictionary = translated_dictionary


class MarkupTranslationRequest:
    def __init__(
        self,
        markup_text: str,
        target_language_code: str,
        source_language_code: str = "",
    ):
        self.markup_text = markup_text
        self.target_language_code = target_language_code
        self.source_language_code = source_language_code


class MarkupTranslationResponse:
    def __init__(self, translated_markup: str):
        self.translated_markup = translated_markup
