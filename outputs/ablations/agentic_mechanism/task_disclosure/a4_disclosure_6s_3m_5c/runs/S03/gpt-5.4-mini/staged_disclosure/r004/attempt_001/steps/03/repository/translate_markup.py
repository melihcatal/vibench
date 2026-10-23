import os
import json
import argparse
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


class SegmentingHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(
            f' {name}' if value is None else f' {name}="{value}"' for name, value in attrs
        )
        self.parts.append(("tag", f"<{tag}{attrs_text}>") )

    def handle_endtag(self, tag):
        self.parts.append(("tag", f"</{tag}>") )

    def handle_startendtag(self, tag, attrs):
        attrs_text = "".join(
            f' {name}' if value is None else f' {name}="{value}"' for name, value in attrs
        )
        self.parts.append(("tag", f"<{tag}{attrs_text} />") )

    def handle_data(self, data):
        self.parts.append(("text", data))

    def handle_entityref(self, name):
        self.parts.append(("text", f"&{name};"))

    def handle_charref(self, name):
        self.parts.append(("text", f"&#{name};"))

    def handle_comment(self, data):
        self.parts.append(("tag", f"<!--{data}-->"))

    def handle_decl(self, decl):
        self.parts.append(("tag", f"<!{decl}>"))


def translate_text_openai(text, target_language, source_language=None, api_key=None):
    if not text:
        return text
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    system = "You are a translation engine. Translate the user's text accurately while preserving meaning, punctuation, and line breaks. Return only the translated text."
    user = f"Translate the following text to {target_language}."
    if source_language:
        user += f" Source language: {source_language}."
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user + "\n\n" + text},
        ],
        "temperature": 0,
    }
    req = Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except (HTTPError, URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Translation failed: {exc}") from exc


def translate_markup(markup, target_language, source_language=None, api_key=None):
    parser = SegmentingHTMLParser()
    parser.feed(markup)
    parser.close()
    translated = []
    for kind, value in parser.parts:
        if kind == "text" and value.strip():
            translated.append(translate_text_openai(value, target_language, source_language, api_key))
        else:
            translated.append(value)
    return "".join(translated)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_language")
    parser.add_argument("input_file", nargs="?")
    parser.add_argument("--source-language")
    parser.add_argument("--api-key")
    args = parser.parse_args()
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            markup = f.read()
    else:
        import sys
        markup = sys.stdin.read()
    print(translate_markup(markup, args.target_language, args.source_language, args.api_key), end="")


if __name__ == "__main__":
    main()
