from html.parser import HTMLParser

from translation_client import TranslationClient
from translation_models import normalize_text

PROVIDER = "GoogleTranslator"


class _MarkupTranslator(HTMLParser):
    def __init__(self, client: TranslationClient, source_language: str, target_language: str):
        super().__init__()
        self.client = client
        self.source_language = source_language
        self.target_language = target_language
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {key}="{value}"' for key, value in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        text = normalize_text(data)
        if text:
            self.parts.append(self.client.translate(text, self.source_language, self.target_language))
        else:
            self.parts.append(data)


def translate_markup(markup: str, source_language: str = "auto", target_language: str = "en") -> str:
    client = TranslationClient()
    parser = _MarkupTranslator(client, source_language, target_language)
    parser.feed(markup)
    return "".join(parser.parts)
