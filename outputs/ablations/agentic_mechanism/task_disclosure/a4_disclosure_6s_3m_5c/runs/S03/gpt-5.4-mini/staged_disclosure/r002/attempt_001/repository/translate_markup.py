import os
import html
import argparse
import requests
from html.parser import HTMLParser


class MarkupTranslator(HTMLParser):
    def __init__(self, source_lang: str, target_lang: str, api_key: str):
        super().__init__(convert_charrefs=False)
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.api_key = api_key
        self.parts = []
        self._text_buffer = []

    def _flush_text(self):
        if not self._text_buffer:
            return
        text = "".join(self._text_buffer)
        self._text_buffer.clear()
        if text.strip():
            self.parts.append(self._translate_text(text))
        else:
            self.parts.append(text)

    def _translate_text(self, text: str) -> str:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"{self.source_lang}|{self.target_lang}",
            "de": "translate_markup.py",
        }
        headers = {"X-API-Key": self.api_key} if self.api_key else {}
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        translated = data.get("responseData", {}).get("translatedText")
        return translated if translated is not None else text

    def handle_starttag(self, tag, attrs):
        self._flush_text()
        attrs_text = "".join(
            f' {name}' if value is None else f' {name}="{html.escape(value, quote=True)}"'
            for name, value in attrs
        )
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self._flush_text()
        self.parts.append(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        self._flush_text()
        attrs_text = "".join(
            f' {name}' if value is None else f' {name}="{html.escape(value, quote=True)}"'
            for name, value in attrs
        )
        self.parts.append(f"<{tag}{attrs_text}/>")

    def handle_data(self, data):
        self._text_buffer.append(data)

    def handle_entityref(self, name):
        self._text_buffer.append(f"&{name};")

    def handle_charref(self, name):
        self._text_buffer.append(f"&#{name};")

    def get_translated(self, markup: str) -> str:
        self.feed(markup)
        self._flush_text()
        return "".join(self.parts)


def translate_markup(markup: str, source_lang: str = "en", target_lang: str = "es") -> str:
    api_key = os.getenv("MYMEMORY_API_KEY", "")
    translator = MarkupTranslator(source_lang, target_lang, api_key)
    return translator.get_translated(markup)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markup")
    parser.add_argument("--source-lang", default="en")
    parser.add_argument("--target-lang", default="es")
    args = parser.parse_args()
    print(translate_markup(args.markup, args.source_lang, args.target_lang))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
