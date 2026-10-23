import os
from html.parser import HTMLParser
from translation_client import get_translation_client


class MarkupParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texts = []
        self.in_tag = False
        self.current_tag = ""

    def handle_starttag(self, tag, attrs):
        self.in_tag = True
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.in_tag = False
        self.current_tag = ""

    def handle_data(self, data):
        if not self.in_tag:
            self.texts.append(data)


def translate_markup(
    markup: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    """Translate HTML or markup while preserving tags.

    Uses Amazon Translate as the concrete provider.
    """
    parser = MarkupParser()
    parser.feed(markup)
    translated_texts = batch_translate(parser.texts, source_lang, target_lang)
    # Reconstruct markup with original tags
    output_parts = []
    text_index = 0
    for token in parser.rawdata.split():
        if token.strip() in parser.texts:
            output_parts.append(translated_texts[text_index])
            text_index += 1
        else:
            output_parts.append(token)
    return "".join(output_parts)
