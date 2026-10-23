import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TranslationRequest:
    text: str
    source_lang: Optional[str] = None
    target_lang: str = "en"
    formality: Optional[str] = None
    preserve_formatting: bool = True
    tag_handling: Optional[str] = None
    outline_detection: bool = True

    def to_deepl_kwargs(self) -> dict:
        kwargs = {}
        if self.source_lang:
            kwargs["source_lang"] = self.source_lang
        if self.formality:
            kwargs["formality"] = self.formality
        kwargs["preserve_formatting"] = self.preserve_formatting
        if self.tag_handling:
            kwargs["tag_handling"] = self.tag_handling
        if self.outline_detection is not None:
            kwargs["outline_detection"] = self.outline_detection
        return kwargs


@dataclass
class TranslationResult:
    text: str
    detected_source_lang: str
    character_count: int


@dataclass
class TranslationResponse:
    results: list[TranslationResult]
    source_lang: str
    target_lang: str
    total_characters: int = 0

    def __post_init__(self):
        if self.total_characters == 0:
            self.total_characters = sum(r.character_count for r in self.results)


@dataclass
class BatchTranslationRequest:
    texts: list[str]
    source_lang: Optional[str] = None
    target_lang: str = "en"
    formality: Optional[str] = None
    preserve_formatting: bool = True


@dataclass
class MarkupTranslationRequest:
    html_text: str
    source_lang: Optional[str] = None
    target_lang: str = "en"
    tag_handling: str = "html"
    formality: Optional[str] = None


@dataclass
class DictionaryTranslationRequest:
    dictionary: dict[str, str]
    source_lang: Optional[str] = None
    target_lang: str = "en"
    formality: Optional[str] = None


def normalize_language_code(code: str) -> str:
    lang_map = {
        "en-us": "EN-US",
        "en-gb": "EN-GB",
        "en": "EN",
        "de": "DE",
        "fr": "FR",
        "es": "ES",
        "it": "IT",
        "pt": "PT",
        "pt-br": "PT-BR",
        "ja": "JA",
        "zh": "ZH",
        "ko": "KO",
        "ru": "RU",
        "nl": "NL",
        "pl": "PL",
        "sv": "SV",
        "da": "DA",
        "fi": "FI",
        "cs": "CS",
        "sk": "SK",
        "ro": "RO",
        "bg": "BG",
        "hu": "HU",
        "el": "EL",
        "tr": "TR",
        "id": "ID",
        "uk": "UK",
        "lv": "LV",
        "lt": "LT",
        "et": "ET",
        "sl": "SL",
    }
    normalized = lang_map.get(code.lower(), code.upper())
    return normalized


def parse_deepl_response(response_text, target_lang: str) -> TranslationResponse:
    results = []
    for text_result in response_text:
        results.append(
            TranslationResult(
                text=text_result.text,
                detected_source_lang=text_result.detected_source_lang,
                character_count=len(text_result.text),
            )
        )
    source = results[0].detected_source_lang if results else ""
    return TranslationResponse(
        results=results,
        source_lang=source,
        target_lang=target_lang,
    )
