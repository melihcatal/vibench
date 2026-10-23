from typing import List, Dict, Any


class TranslationRequest:
    def __init__(
        self,
        texts: List[str],
        target_language: str,
        source_language: str = None,
        format: str = None,
    ):
        self.texts = texts
        self.target_language = target_language
        self.source_language = source_language
        self.format = format


class TranslationResponse:
    def __init__(self, translated_texts: List[str]):
        self.translated_texts = translated_texts

    def to_list(self) -> List[str]:
        return self.translated_texts


class DictionaryTranslationRequest:
    def __init__(
        self,
        dictionary: Dict[str, str],
        target_language: str,
        source_language: str = None,
    ):
        self.dictionary = dictionary
        self.target_language = target_language
        self.source_language = source_language


class DictionaryTranslationResponse:
    def __init__(self, translated_dictionary: Dict[str, str]):
        self.translated_dictionary = translated_dictionary

    def to_dict(self) -> Dict[str, str]:
        return self.translated_dictionary
