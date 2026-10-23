import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TranslationRequest:
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"
    formality: Optional[str] = None
    preserve_formatting: bool = True
    split_sentences: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    texts: list[str]
    source_lang: str = "auto"
    target_lang: str = "en"
    formality: Optional[str] = None
    preserve_formatting: bool = True
    split_sentences: Optional[str] = None


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_lang: str = "auto"
    target_lang: str = "en"
    tag_handling: str = "html"
    formality: Optional[str] = None
    preserve_formatting: bool = True
    split_sentences: Optional[str] = None
    non_splitting_tags: list[str] = field(default_factory=list)
    ignore_tags: list[str] = field(default_factory=list)


@dataclass
class DictionaryTranslationRequest:
    data: dict[str, str]
    source_lang: str = "auto"
    target_lang: str = "en"
    formality: Optional[str] = None
    preserve_formatting: bool = True


@dataclass
class TranslationResponse:
    translated_text: str
    source_lang: str
    target_lang: str
    char_count: int
    detected_source_lang: Optional[str] = None


@dataclass
class BatchTranslationResponse:
    translations: list[TranslationResponse]
    total_char_count: int

    def translated_texts(self) -> list[str]:
        return [t.translated_text for t in self.translations]


@dataclass
class MarkupTranslationResponse:
    translated_markup: str
    source_lang: str
    target_lang: str
    char_count: int


@dataclass
class DictionaryTranslationResponse:
    translated_data: dict[str, str]
    source_lang: str
    target_lang: str
    total_char_count: int


def normalize_language_code(code: str) -> str:
    lang_map = {
        "en": "EN",
        "en-us": "EN-US",
        "en-gb": "EN-GB",
        "de": "DE",
        "fr": "FR",
        "es": "ES",
        "it": "IT",
        "pt": "PT",
        "pt-br": "PT-BR",
        "pt-pt": "PT-PT",
        "ja": "JA",
        "zh": "ZH",
        "zh-cn": "ZH",
        "zh-tw": "ZH",
        "ko": "KO",
        "ru": "RU",
        "ar": "AR",
        "bg": "BG",
        "cs": "CS",
        "da": "DA",
        "el": "EL",
        "et": "ET",
        "fi": "FI",
        "hu": "HU",
        "id": "ID",
        "lv": "LV",
        "lt": "LT",
        "nb": "NB",
        "nl": "NL",
        "pl": "PL",
        "ro": "RO",
        "sk": "SK",
        "sl": "SL",
        "sv": "SV",
        "tr": "TR",
        "uk": "UK",
    }
    return lang_map.get(code.lower(), code.upper())


def normalize_source_lang(detected: Optional[str]) -> str:
    if detected is None:
        return "auto"
    return normalize_language_code(detected)


def build_translation_request_params(request: TranslationRequest) -> dict:
    params = {
        "target_lang": normalize_language_code(request.target_lang),
        "preserve_formatting": request.preserve_formatting,
    }
    if request.source_lang and request.source_lang.lower() != "auto":
        params["source_lang"] = normalize_language_code(request.source_lang)
    if request.formality:
        params["formality"] = request.formality
    if request.split_sentences:
        params["split_sentences"] = request.split_sentences
    return params
