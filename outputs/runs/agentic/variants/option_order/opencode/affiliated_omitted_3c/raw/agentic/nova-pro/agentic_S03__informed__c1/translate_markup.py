from google.cloud import translate_v2 as translate
import re


def translate_markup(markup, target_language):
    client = translate.Client()
    pattern = re.compile(r"<[^>]+>")
    tags = pattern.findall(markup)
    content = pattern.sub("", markup)
    translated_content = client.translate(content, target_language=target_language)[
        "translatedText"
    ]
    translated_markup = translated_content
    for tag in tags:
        translated_markup = translated_markup.replace(content, tag, 1)
    return translated_markup
