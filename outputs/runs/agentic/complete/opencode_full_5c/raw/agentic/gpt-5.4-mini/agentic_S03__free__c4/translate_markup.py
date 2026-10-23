from html.parser import HTMLParser

from openai import OpenAI

from translation_client import (
    build_translation_messages,
    get_openai_client,
    chat_completion,
)


class TagPreservingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join([f' {k}="{v}"' for k, v in attrs])
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(data)


def translate_markup(source_language: str, target_language: str, markup: str) -> str:
    client: OpenAI = get_openai_client()
    parser = TagPreservingParser()
    parser.feed(markup)
    translated = chat_completion(
        client, build_translation_messages(source_language, target_language, markup)
    )
    return translated if translated else "".join(parser.parts)
