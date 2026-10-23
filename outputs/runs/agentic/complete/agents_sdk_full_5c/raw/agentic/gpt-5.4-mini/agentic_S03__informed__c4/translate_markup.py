from __future__ import annotations

from html.parser import HTMLParser

from translation_client import translate_text as deepl_translate_text


class _MarkupTranslator(HTMLParser):
    def __init__(self, source_language: str, target_language: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source_language = source_language
        self.target_language = target_language
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_str = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            self.parts.append(deepl_translate_text(data, self.source_language, self.target_language))
        else:
            self.parts.append(data)

    def handle_startendtag(self, tag, attrs):
        attrs_str = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_str} />")


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    parser = _MarkupTranslator(source_language, target_language)
    parser.feed(markup)
    return "".join(parser.parts)
