import os
from google.cloud import translate_v2 as translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

translate_client = translate.Client()


def translate_markup(markup, target_language):
    result = translate_client.translate(
        markup, target_language=target_language, format_="html"
    )
    return result["translatedText"]
