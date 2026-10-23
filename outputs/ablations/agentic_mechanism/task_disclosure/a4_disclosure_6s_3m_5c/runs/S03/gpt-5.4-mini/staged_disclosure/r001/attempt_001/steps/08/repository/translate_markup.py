import argparse
import os
import re
from html.parser import HTMLParser
from html import unescape

import requests


class MarkupPreservingTranslator(HTMLParser):
    def __init__(self, translate_fn):
        super().__init__(convert_charrefs=False)
        self.translate_fn = translate_fn
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {name}' if value is None else f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        attrs_text = "".join(f' {name}' if value is None else f' {name}="{value}"' for name, value in attrs)
        self.parts.append(f"<{tag}{attrs_text} />")

    def handle_comment(self, data):
        self.parts.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.parts.append(f"<!{decl}>")

    def handle_pi(self, data):
        self.parts.append(f"<?{data}>")

    def handle_data(self, data):
        if data.strip():
            translated = self.translate_fn(data)
            self.parts.append(translated)
        else:
            self.parts.append(data)

    def translate(self, markup: str) -> str:
        self.parts = []
        self.feed(markup)
        self.close()
        return "".join(self.parts)


def deepl_translate(text: str, target_language: str, source_language: str | None = None) -> str:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    payload = {"text": text, "target_lang": target_language.upper()}
    if source_language:
        payload["source_lang"] = source_language.upper()
    response = requests.post("https://api-free.deepl.com/v2/translate", data=payload, headers={"Authorization": f"DeepL-Auth-Key {auth_key}"}, timeout=30)
    response.raise_for_status()
    return response.json()["translations"][0]["text"]


def translate_markup(markup: str, target_language: str, source_language: str | None = None) -> str:
    translator = MarkupPreservingTranslator(lambda text: deepl_translate(unescape(text), target_language, source_language))
    return translator.translate(markup)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("markup")
    parser.add_argument("target_language")
    parser.add_argument("--source-language")
    args = parser.parse_args()
    print(translate_markup(args.markup, args.target_language, args.source_language))


if __name__ == "__main__":
    main()
