# [SAME-SCENARIO] translate_markup.py

import os
from google.cloud import translate_v2 as translate

# Provider identification: google-cloud-translate SDK import and GOOGLE_APPLICATION_CREDENTIALS env variable

def translate_markup(source_markup: str, target_language: str = "es") -> str:
    """Translate HTML or markup while preserving tags.

    Args:
        source_markup (str): HTML/markup string to translate.
        target_language (str): Target language code (default: "es").

    Returns:
        str: Translated markup with original tags intact.
    """
    client = translate.Client()
    # The translate service automatically preserves tags that are not translatable
    result = client.translate(source_markup, target_language=target_language)
    return result["translatedText"]

# Simple demo
if __name__ == "__main__":
    html = """<p>Hello <strong>world</strong>!</p>""
    print("Original:", html)
    print("Translated:", translate_markup(html))
