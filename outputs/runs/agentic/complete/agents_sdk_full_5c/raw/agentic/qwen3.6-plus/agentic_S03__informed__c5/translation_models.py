"""
translation_models.py - Define local request, response, and normalization helpers
for General Text Translation using DeepL API.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import html


@dataclass
class TranslationRequest:
    """Request model for a single translation."""
    text: str
    source_lang: Optional[str] = None
    target_lang: str = "en"
    preserve_formatting: bool = True
    formal: bool = False


@dataclass
class TranslationResponse:
    """Response model for a single translation."""
    translated_text: str
    source_lang: str
    target_lang: str
    detected_source: bool = False
    character_count: int = 0
    billing_characters: int = 0


@dataclass
class BatchTranslationRequest:
    """Request model for batch translation."""
    texts: List[str]
    source_lang: Optional[str] = None
    target_lang: str = "en"
    preserve_formatting: bool = True
    preserve_order: bool = True


@dataclass
class BatchTranslationResponse:
    """Response model for batch translation."""
    translations: List[str] = field(default_factory=list)
    source_lang: str = ""
    target_lang: str = ""
    total_characters: int = 0


@dataclass
class DictionaryTranslationRequest:
    """Request model for dictionary value translation."""
    data: Dict[str, Any]
    source_lang: Optional[str] = None
    target_lang: str = "en"
    keys_to_skip: Optional[List[str]] = None


@dataclass
class DictionaryTranslationResponse:
    """Response model for dictionary value translation."""
    translated_data: Dict[str, Any] = field(default_factory=dict)
    source_lang: str = ""
    target_lang: str = ""
    translated_keys: List[str] = field(default_factory=list)


def normalize_source_lang(source_lang: Optional[str]) -> Optional[str]:
    """Normalize source language code to DeepL format (uppercase)."""
    if source_lang is None:
        return None
    return source_lang.upper()


def normalize_target_lang(target_lang: str) -> str:
    """Normalize target language code to DeepL format (uppercase with regional variant)."""
    lang = target_lang.upper()
    regional_mapping = {
        "EN": "EN-US",
        "PT": "PT-BR",
        "ZH": "ZH",
        "ES": "ES",
        "FR": "FR",
        "DE": "DE",
        "IT": "IT",
        "JA": "JA",
        "KO": "KO",
        "NL": "NL",
        "PL": "PL",
        "RU": "RU",
        "SV": "SV",
        "TR": "TR",
    }
    return regional_mapping.get(lang, lang)


def extract_text_from_markup(html_content: str) -> List[Dict[str, Any]]:
    """Extract translatable text segments from HTML/markup while preserving tag positions."""
    segments = []
    current_text = []
    current_tags = []
    i = 0
    in_tag = False
    tag_start = 0

    while i < len(html_content):
        if html_content[i] == '<':
            in_tag = True
            tag_start = i
            if current_text:
                segments.append({
                    "type": "text",
                    "content": "".join(current_text),
                    "tags_before": list(current_tags)
                })
                current_text = []
            current_tags.append(html_content[i])
            while i < len(html_content) and html_content[i] != '>':
                current_tags.append(html_content[i])
                i += 1
            current_tags.append('>')
            in_tag = False
        else:
            if in_tag:
                current_tags.append(html_content[i])
            else:
                current_text.append(html_content[i])
        i += 1

    if current_text:
        segments.append({
            "type": "text",
            "content": "".join(current_text),
            "tags_before": list(current_tags)
        })
    if current_tags:
        segments.append({
            "type": "tag",
            "content": "".join(current_tags),
            "tags_before": []
        })

    return segments


def rebuild_markup(segments: List[Dict[str, Any]], translated_texts: List[str]) -> str:
    """Rebuild HTML/markup from segments with translated text content."""
    result = []
    text_index = 0
    for seg in segments:
        if seg["type"] == "tag":
            result.append(seg["content"])
        elif seg["type"] == "text":
            if text_index < len(translated_texts):
                result.append(translated_texts[text_index])
                text_index += 1
            else:
                result.append(seg["content"])
    return "".join(result)


def html_unescape(text: str) -> str:
    """Unescape HTML entities in text."""
    return html.unescape(text)


def html_escape(text: str) -> str:
    """Escape HTML entities in text."""
    return html.escape(text, quote=False)
