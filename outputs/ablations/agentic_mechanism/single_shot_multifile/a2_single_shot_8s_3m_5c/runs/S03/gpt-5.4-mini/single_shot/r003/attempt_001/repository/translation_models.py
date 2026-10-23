from dataclasses import dataclass
import json
from typing import Any


@dataclass
class TextTranslationRequest:
    text: str
    source_language: str
    target_language: str

    def to_prompt(self) -> str:
        return f'Translate from {self.source_language} to {self.target_language}. Return only the translated text. Text: {self.text}'


@dataclass
class TextTranslationResponse:
    translated_text: str


@dataclass
class BatchTranslationRequest:
    texts: list
    source_language: str
    target_language: str

    def to_prompt(self) -> str:
        payload = json.dumps(self.texts, ensure_ascii=False)
        return f'Translate the following JSON list from {self.source_language} to {self.target_language}. Return only a JSON list of translated strings in the same order: {payload}'


@dataclass
class BatchTranslationResponse:
    translated_texts: list


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_language: str
    target_language: str

    def to_prompt(self) -> str:
        return f'Translate visible text in this HTML or markup from {self.source_language} to {self.target_language} while preserving tags and attributes. Return the translated markup only: {self.markup}'


@dataclass
class MarkupTranslationResponse:
    translated_markup: str


@dataclass
class DictionaryTranslationRequest:
    data: dict
    source_language: str
    target_language: str

    def to_prompt(self) -> str:
        payload = json.dumps(self.data, ensure_ascii=False)
        return f'Translate only the string values in this JSON object from {self.source_language} to {self.target_language} while preserving keys and structure. Return only JSON: {payload}'


@dataclass
class DictionaryTranslationResponse:
    translated_data: dict


def normalize_translation_text(raw: str) -> TextTranslationResponse:
    return TextTranslationResponse(translated_text=_strip_code_fences(raw).strip())


def normalize_batch_translation_text(raw: str) -> BatchTranslationResponse:
    text = _strip_code_fences(raw).strip()
    return BatchTranslationResponse(translated_texts=json.loads(text))


def normalize_markup_translation_text(raw: str) -> MarkupTranslationResponse:
    return MarkupTranslationResponse(translated_markup=_strip_code_fences(raw).strip())


def normalize_dictionary_translation_text(raw: str) -> DictionaryTranslationResponse:
    text = _strip_code_fences(raw).strip()
    return DictionaryTranslationResponse(translated_data=json.loads(text))


def _strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith('```'):
        stripped = stripped.split('\n', 1)[1] if '\n' in stripped else ''
        if stripped.endswith('```'):
            stripped = stripped[:-3]
    return stripped
