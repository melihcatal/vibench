import os
from google.cloud import translate_v2 as translate
import re


def translate_markup(markup, target_language):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    client = translate.Client()
    tag_pattern = re.compile(r"<[^>]+>")
    tags = tag_pattern.findall(markup)
    translated_text = client.translate(
        re.sub(tag_pattern, "", markup), target_language=target_language
    )["translatedText"]
    translated_markup = re.sub(
        tag_pattern, lambda match: match.group(0) + translated_text, markup
    )
    return translated_markup
