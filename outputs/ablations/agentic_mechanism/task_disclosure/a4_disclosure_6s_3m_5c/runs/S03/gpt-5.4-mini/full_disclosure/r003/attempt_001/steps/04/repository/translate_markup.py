import os
import re
from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from typing import List, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"


@dataclass
class Segment:
    kind: str
    value: str


class _MarkupTokenizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.segments: List[Segment] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(
            f' {name}' if value is None else f' {name}="{escape(value, quote=True)}"'
            for name, value in attrs
        )
        self.segments.append(Segment("tag", f"<{tag}{attrs_text}>") )

    def handle_endtag(self, tag):
        self.segments.append(Segment("tag", f"</{tag}>") )

    def handle_startendtag(self, tag, attrs):
        attrs_text = "".join(
            f' {name}' if value is None else f' {name}="{escape(value, quote=True)}"'
            for name, value in attrs
        )
        self.segments.append(Segment("tag", f"<{tag}{attrs_text}/>") )

    def handle_data(self, data):
        self.segments.append(Segment("text", data))

    def handle_entityref(self, name):
        self.segments.append(Segment("tag", f"&{name};"))

    def handle_charref(self, name):
        self.segments.append(Segment("tag", f"&#{name};"))

    def handle_comment(self, data):
        self.segments.append(Segment("tag", f"<!--{data}-->"))

    def handle_decl(self, decl):
        self.segments.append(Segment("tag", f"<!{decl}>"))


def _translate_text_openai(text: str, source_language: str, target_language: str, model: str = "gpt-5.4-mini") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"Translate from {source_language} to {target_language}. Return only the translated text.",
                    }
                ],
            },
            {"role": "user", "content": [{"type": "text", "text": text}]},
        ],
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                return content["text"].strip()
    raise RuntimeError("OpenAI response did not contain translated text")


def translate_markup(markup: str, source_language: str, target_language: str, model: str = "gpt-5.4-mini") -> str:
    tokenizer = _MarkupTokenizer()
    tokenizer.feed(markup)
    translated: List[str] = []
    for segment in tokenizer.segments:
        if segment.kind == "text" and segment.value.strip():
            translated.append(_translate_text_openai(segment.value, source_language, target_language, model))
        else:
            translated.append(segment.value)
    return "".join(translated)
