from typing import TypedDict, Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class LanguageCode(str, Enum):
    EN = "EN"
    ES = "ES"
    FR = "FR"
    DE = "DE"
    IT = "IT"
    JA = "JA"
    ZH = "ZH"
    KO = "KO"
    PT = "PT"
    RU = "RU"
    AR = "AR"


class Formality(str, Enum):
    DEFAULT = "default"
    MORE = "more"
    LESS = "less"
    PREFER_MORE = "prefer_more"
    PREFER_LESS = "prefer_less"


@dataclass
class TranslationRequest:
    text: str
    target_lang: str
    source_lang: Optional[str] = None
    formality: Optional[Formality] = None
    preserve_formatting: bool = False
    glossary_id: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None
    character_count: Optional[int] = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    target_lang: str
    source_lang: Optional[str] = None
    formality: Optional[Formality] = None
    preserve_formatting: bool = False


@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    detected_source_language: Optional[str] = None
    character_count: Optional[int] = None


@dataclass
class MarkupTranslationRequest:
    markup_text: str
    target_lang: str
    source_lang: Optional[str] = None
    tag_handling: str = "html"
    outline_detection: bool = True
    non_splitting_tags: Optional[List[str]] = None


@dataclass
class MarkupTranslationResponse:
    translated_markup: str
    detected_source_language: Optional[str] = None
    character_count: Optional[int] = None


@dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, Any]
    target_lang: str
    source_lang: Optional[str] = None
    formality: Optional[Formality] = None
    preserve_formatting: bool = False
    skip_keys: Optional[List[str]] = None


@dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, Any]
    detected_source_language: Optional[str] = None
    character_count: Optional[int] = None


def normalize_language_code(lang_code: str) -> str:
    lang_code = lang_code.upper()
    if lang_code in ["EN", "EN-US", "EN-GB"]:
        return "EN"
    if lang_code in ["ZH", "ZH-CN", "ZH-TW"]:
        return "ZH"
    return lang_code


def validate_language_code(lang_code: str) -> bool:
    try:
        LanguageCode(lang_code.upper())
        return True
    except ValueError:
        return False


def extract_text_from_dict_values(
    dictionary: Dict[str, Any], skip_keys: Optional[List[str]] = None
) -> Dict[str, str]:
    skip_keys = skip_keys or []
    text_dict = {}
    for key, value in dictionary.items():
        if key in skip_keys:
            continue
        if isinstance(value, str):
            text_dict[key] = value
        elif isinstance(value, (int, float)):
            text_dict[key] = str(value)
        elif value is None:
            text_dict[key] = ""
    return text_dict


def reconstruct_dict_with_translations(
    original_dict: Dict[str, Any],
    translated_texts: Dict[str, str],
    skip_keys: Optional[List[str]] = None,
) -> Dict[str, Any]:
    skip_keys = skip_keys or []
    result = original_dict.copy()
    for key, value in original_dict.items():
        if key in skip_keys:
            continue
        if key in translated_texts:
            result[key] = translated_texts[key]
    return result
