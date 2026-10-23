from google.cloud import translate_v2 as translate
import os


def translate_markup(
    html_content: str, target_language: str, source_language: str = None
) -> str:
    """Translates HTML or markup while preserving tags using Google Cloud Translation."""
    client = translate.Client()
    # Google Cloud Translation automatically detects markup and preserves tags
    result = client.translate(
        html_content,
        target_language=target_language,
        source_language=source_language,
        format="html",
    )
    return result["translatedText"]


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "path/to/your/google_credentials.json"
    )

    html_to_translate = "<p>Hello, <b>world</b>!</p>"
    target_lang = "de"
    translated_html = translate_markup(html_to_translate, target_lang)
    print(f"Original: {html_to_translate}, Translated: {translated_html}")
