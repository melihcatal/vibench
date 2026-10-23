from html.parser import HTMLParser
from typing import List

from translation_client import create_translation_client, target_language_code
from translation_models import strip_markup_text


class _MarkupTranslator(HTMLParser):
    def __init__(self, client, source_language: str, target_language: str):
        super().__init__()
        self.client = client
        self.source_language = source_language
        self.target_language = target_language
        self.parts: List[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_str = ''.join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f'<{tag}{attrs_str}>')

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')

    def handle_startendtag(self, tag, attrs):
        attrs_str = ''.join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f'<{tag}{attrs_str} />')

    def handle_data(self, data):
        text = strip_markup_text(data)
        if text.strip():
            result = self.client.translate_text(text, source_lang=target_language_code(self.source_language), target_lang=target_language_code(self.target_language))
            self.parts.append(result.text)
        else:
            self.parts.append(data)


def translate_markup(source_language: str, target_language: str, markup: str) -> str:
    client = create_translation_client()
    parser = _MarkupTranslator(client, source_language, target_language)
    parser.feed(markup)
    parser.close()
    return ''.join(parser.parts)
