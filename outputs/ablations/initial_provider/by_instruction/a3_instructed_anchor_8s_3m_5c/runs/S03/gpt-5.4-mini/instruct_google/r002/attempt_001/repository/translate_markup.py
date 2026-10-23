from html.parser import HTMLParser

from translation_client import get_default_source_language, get_default_target_language, get_translation_client


class _MarkupTranslator(HTMLParser):
    def __init__(self, source_language, target_language):
        super().__init__()
        self.source_language = source_language
        self.target_language = target_language
        self.parts = []
        self.client = get_translation_client()

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {k}="{v}"' for k, v in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            translated = self.client.translate(data, source_language=self.source_language, target_language=self.target_language)["translatedText"]
            self.parts.append(translated)
        else:
            self.parts.append(data)


def translate_markup(markup: str, source_language: str = None, target_language: str = None) -> str:
    parser = _MarkupTranslator(source_language or get_default_source_language(), target_language or get_default_target_language())
    parser.feed(markup)
    return "".join(parser.parts)
