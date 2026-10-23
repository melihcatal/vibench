import os
from google.cloud import translate_v2 as translate


def stored_text_translate(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)

    print(f"Translation: {result['translatedText']}")
    return result["translatedText"]
