from __future__ import annotations

from html.parser import HTMLParser
from typing import List, Tuple

from translation_client import translate_text as deepl_translate_text
from translation_models import TranslationResult


class _MarkupTranslator(HTMLParser):
    def __init__(self, source_language: str, target_language: str) -> None:
        super().__init__(convert_charrefs=False)
        self.source_language = source_language
        self.target_language = target_language
        self.parts: List[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            translated = deepl_translate_text(data, self.source_language, self.target_language)["translated_text"]
            self.parts.append(translated)
        else:
            self.parts.append(data)

    def handle_startendtag(self, tag, attrs):
        attrs_text = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_text}/>")


def translate_markup(markup: str, source_language: str, target_language: str) -> TranslationResult:
    parser = _MarkupTranslator(source_language, target_language)
    parser.feed(markup)
    return TranslationResult(
        translated_text="".join(parser.parts),
        source_language=source_language,
        target_language=target_language,
        provider="deepl",
        metadata={"model": "deepl-pro", "format": "html"},
    )
