from __future__ import annotations

from html.parser import HTMLParser
from typing import List

from translation_client import get_amazon_translate_client, load_translation_config
from translation_models import normalize_language_code


class _MarkupTranslator(HTMLParser):
    def __init__(self, client, source_language: str, target_language: str) -> None:
        super().__init__(convert_charrefs=False)
        self.client = client
        self.source_language = source_language
        self.target_language = target_language
        self.parts: List[str] = []

    def handle_starttag(self, tag, attrs):
        attr_text = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attr_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            translated = self.client.translate_text(Text=data, SourceLanguageCode=self.source_language, TargetLanguageCode=self.target_language)
            self.parts.append(translated["TranslatedText"])
        else:
            self.parts.append(data)

    def handle_startendtag(self, tag, attrs):
        attr_text = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attr_text} />")


def translate_markup(markup: str, source_language: str | None = None, target_language: str | None = None) -> str:
    config = load_translation_config()
    source = normalize_language_code(source_language or config.source_language or "auto")
    target = normalize_language_code(target_language or config.target_language or "en")
    client = get_amazon_translate_client(config)
    parser = _MarkupTranslator(client, source, target)
    parser.feed(markup)
    return "".join(parser.parts)
