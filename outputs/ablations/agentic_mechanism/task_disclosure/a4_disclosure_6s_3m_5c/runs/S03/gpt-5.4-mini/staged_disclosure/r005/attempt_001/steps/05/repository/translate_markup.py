import os
from html.parser import HTMLParser
from typing import List

from deepl import DeepLClient


class _MarkupTranslator(HTMLParser):
    def __init__(self, target_lang: str, client: DeepLClient):
        super().__init__(convert_charrefs=False)
        self.target_lang = target_lang
        self.client = client
        self.parts: List[str] = []
        self._buffer: List[str] = []

    def _flush_text(self) -> None:
        if not self._buffer:
            return
        text = "".join(self._buffer)
        self._buffer.clear()
        if text.strip():
            result = self.client.translate_text(text, target_lang=self.target_lang)
            translated = result.text if hasattr(result, "text") else str(result)
            self.parts.append(translated)
        else:
            self.parts.append(text)

    def handle_starttag(self, tag, attrs):
        self._flush_text()
        attrs_str = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        self._flush_text()
        self.parts.append(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        self._flush_text()
        attrs_str = "".join(f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_str}/>")

    def handle_data(self, data):
        self._buffer.append(data)

    def handle_entityref(self, name):
        self._buffer.append(f"&{name};")

    def handle_charref(self, name):
        self._buffer.append(f"&#{name};")

    def handle_comment(self, data):
        self._flush_text()
        self.parts.append(f"<!--{data}-->")

    def translate(self, markup: str) -> str:
        self.feed(markup)
        self._flush_text()
        return "".join(self.parts)


def translate_markup(markup: str, target_lang: str, auth_key: str | None = None) -> str:
    key = auth_key or os.getenv("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    client = DeepLClient(auth_key=key)
    return _MarkupTranslator(target_lang=target_lang, client=client).translate(markup)
