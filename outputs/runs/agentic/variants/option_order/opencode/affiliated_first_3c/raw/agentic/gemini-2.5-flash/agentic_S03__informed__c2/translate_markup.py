from google.cloud import translate_v2 as translate
import os


def translate_html_markup(
    html: str, target_language: str, source_language: str = None
) -> str:
    client = translate.Client()
    result = client.translate(
        html,
        target_language=target_language,
        source_language=source_language,
        format_="html",
    )
    return result["translatedText"]
