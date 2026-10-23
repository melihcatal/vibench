from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class TranslationRequest:
    text: str = ""
    source_lang: str = ""
    target_lang: str = "en"
    preserve_formatting: bool = True
    tag_handling: str = "html"
    split_sentences: str = "1"
    formality: str = "default"


@dataclass
class TranslationResult:
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    character_count: int = 0
    billing_character_count: int = 0


@dataclass
class BatchTranslationRequest:
    texts: List[str] = field(default_factory=list)
    source_lang: str = ""
    target_lang: str = "en"
    preserve_formatting: bool = True
    tag_handling: str = "html"


@dataclass
class BatchTranslationResult:
    results: List[TranslationResult] = field(default_factory=list)
    total_characters: int = 0


@dataclass
class MarkupTranslationRequest:
    content: str = ""
    source_lang: str = ""
    target_lang: str = "en"
    tag_handling: str = "html"
    ignore_tags: Optional[List[str]] = None
    outline_detection: bool = False


@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, str] = field(default_factory=dict)
    source_lang: str = ""
    target_lang: str = "en"
    preserve_keys: bool = True


@dataclass
class DictionaryTranslationResult:
    translated_data: Dict[str, str] = field(default_factory=dict)
    key_mapping: Dict[str, str] = field(default_factory=dict)


def normalize_language_code(code: str) -> str:
    code = code.strip().upper()
    lang_map = {
        "EN": "EN",
        "EN-US": "EN-US",
        "EN-GB": "EN-GB",
        "DE": "DE",
        "FR": "FR",
        "ES": "ES",
        "IT": "IT",
        "PT": "PT",
        "PT-BR": "PT-BR",
        "PT-PT": "PT-PT",
        "NL": "NL",
        "PL": "PL",
        "RU": "RU",
        "JA": "JA",
        "ZH": "ZH",
        "KO": "KO",
        "AR": "AR",
        "BG": "BG",
        "CS": "CS",
        "DA": "DA",
        "EL": "EL",
        "ET": "ET",
        "FI": "FI",
        "HU": "HU",
        "ID": "ID",
        "LT": "LT",
        "LV": "LV",
        "NB": "NB",
        "RO": "RO",
        "SK": "SK",
        "SL": "SL",
        "SV": "SV",
        "TR": "TR",
        "UK": "UK",
    }
    return lang_map.get(code, code)


def build_translation_payload(request: TranslationRequest) -> dict:
    payload = {
        "target_lang": normalize_language_code(request.target_lang),
        "preserve_formatting": request.preserve_formatting,
        "tag_handling": request.tag_handling,
        "split_sentences": request.split_sentences,
    }
    if request.source_lang:
        payload["source_lang"] = normalize_language_code(request.source_lang)
    if request.formality != "default":
        payload["formality"] = request.formality
    return payload


def parse_translation_response(
    response_text: str, response_info: dict
) -> TranslationResult:
    return TranslationResult(
        translated_text=response_text,
        source_language=response_info.get("source_lang", ""),
        target_language=response_info.get("target_lang", ""),
        character_count=len(response_text),
        billing_character_count=response_info.get("billing_chars", len(response_text)),
    )
