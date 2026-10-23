"""
Translation request, response, and normalization helpers for General Text Translation.
Provides data models and utility functions for translation payloads.
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from html.parser import HTMLParser
import re
import html


@dataclass
class TranslationRequest:
    """Normalized translation request model."""
    source_text: str
    source_language: str
    target_language: str
    format: str = "text"  # text, html, srt
    glossary: Optional[Dict[str, str]] = None
    model: Optional[str] = None


@dataclass
class TranslationResponse:
    """Normalized translation response model."""
    translated_text: str
    source_language: str
    target_language: str
    confidence: float = 1.0
    model_used: Optional[str] = None
    character_count: int = 0


@dataclass
class BatchTranslationRequest:
    """Batch translation request model."""
    texts: List[str]
    source_language: str
    target_language: str
    format: str = "text"


@dataclass
class BatchTranslationResponse:
    """Batch translation response model."""
    translations: List[TranslationResponse]
    total_characters: int = 0


@dataclass
class MarkupTranslationRequest:
    """HTML/Markup translation request model."""
    html_content: str
    source_language: str
    target_language: str
    preserve_formatting: bool = True


@dataclass
class DictionaryTranslationRequest:
    """Dictionary translation request model."""
    data: Dict[str, str]
    source_language: str
    target_language: str
    translate_keys: bool = False


class TagPreservingParser(HTMLParser):
    """HTML parser that extracts translatable text while preserving tag positions."""

    def __init__(self):
        super().__init__()
        self.segments = []
        self.tag_stack = []
        self.current_text = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        if self.current_text:
            self.segments.append({
                "type": "text",
                "content": "".join(self.current_text),
                "tags": list(self.tag_stack)
            })
            self.current_text = []
        self.tag_stack.append(tag)
        self.segments.append({
            "type": "tag",
            "content": self.get_starttag_text()
        })

    def handle_endtag(self, tag):
        if self.current_text:
            self.segments.append({
                "type": "text",
                "content": "".join(self.current_text),
                "tags": list(self.tag_stack)
            })
            self.current_text = []
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        self.segments.append({
            "type": "tag",
            "content": f"</{tag}>"
        })

    def handle_data(self, data):
        if data.strip():
            self.current_text.append(data)

    def handle_entityref(self, name):
        self.current_text.append(f"&{name};")

    def handle_charref(self, name):
        self.current_text.append(f"&#{name};")

    def get_extracted_texts(self) -> List[str]:
        """Get list of translatable text segments."""
        return [s["content"] for s in self.segments if s["type"] == "text"]


def normalize_language_code(code: str) -> str:
    """Normalize language code to BCP-47 format expected by Google Cloud Translation."""
    code = code.strip().lower()
    replacements = {
        "zh": "zh-CN",
        "no": "no-NO",
        "pt": "pt-PT",
        "es": "es-ES",
        "fr": "fr-FR",
        "de": "de-DE",
        "ja": "ja",
        "ko": "ko",
        "en": "en-US",
    }
    return replacements.get(code, code)


def build_translation_payload(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    mime_type: str = "text/plain",
    model: Optional[str] = None
) -> Dict[str, Any]:
    """Build a normalized payload for Google Cloud Translation v3 API."""
    payload = {
        "contents": [text],
        "target_language_code": normalize_language_code(target_language),
        "mime_type": mime_type,
    }
    if source_language:
        payload["source_language_code"] = normalize_language_code(source_language)
    if model:
        payload["model"] = model
    return payload


def parse_translation_response(response: Any) -> TranslationResponse:
    """Parse Google Cloud Translation v3 response into normalized model."""
    if hasattr(response, "translations"):
        translation = response.translations[0]
        return TranslationResponse(
            translated_text=translation.translated_text,
            source_language=response.source_language_code or "auto",
            target_language=translation.detected_language_code or response.target_language_code,
            confidence=getattr(translation, "detected_language_confidence", 1.0),
            model_used=getattr(response, "model", None),
            character_count=len(translation.translated_text),
        )
    return TranslationResponse(
        translated_text=str(response),
        source_language="auto",
        target_language="unknown",
    )


def split_html_content(html_string: str) -> Dict[str, Any]:
    """Split HTML into translatable segments and structural markers."""
    parser = TagPreservingParser()
    parser.feed(html_string)
    
    texts = []
    text_indices = []
    
    for i, segment in enumerate(parser.segments):
        if segment["type"] == "text":
            texts.append(segment["content"])
            text_indices.append(i)
    
    return {
        "segments": parser.segments,
        "translatable_texts": texts,
        "text_indices": text_indices,
    }


def reassemble_html(segments: List[Dict], translated_texts: List[str]) -> str:
    """Reassemble HTML from segments and translated texts."""
    text_idx = 0
    result_parts = []
    
    for segment in segments:
        if segment["type"] == "tag":
            result_parts.append(segment["content"])
        elif segment["type"] == "text" and text_idx < len(translated_texts):
            result_parts.append(html.escape(translated_texts[text_idx]))
            text_idx += 1
    
    return "".join(result_parts)
