from __future__ import annotations

from html.parser import HTMLParser

from translation_client import get_client, normalize_language_code
from translation_models import MarkupTranslationResult


class _MarkupTranslator(HTMLParser):
    def __init__(self, client, source_language: str, target_language: str):
        super().__init__(convert_charrefs=False)
        self.client = client
        self.source_language = source_language
        self.target_language = target_language
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {k}="{v}"' for k, v in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            translated = self.client.translate(
                data,
                source_language=self.source_language,
                target_language=self.target_language,
                format_="text",
            )["translatedText"]
            self.parts.append(translated)
        else:
            self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")


def translate_markup(markup: str, source_language: str, target_language: str) -> MarkupTranslationResult:
    client = get_client()
    parser = _MarkupTranslator(client, normalize_language_code(source_language), normalize_language_code(target_language))
    parser.feed(markup)
    parser.close()
    return MarkupTranslationResult(translated_markup="".join(parser.parts))
