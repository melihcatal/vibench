import os
from translation_client import get_translation_client

def translate_html_markup(html_content: str, target_language: str, source_language: str = "en") -> str:
    """Translates HTML or markup while preserving tags using Google Cloud Translation."""
    client = get_translation_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[html_content],
        mime_type="text/html",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_html = response.translations[0].translated_text
    return translated_html

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars)
    # html_to_translate = "<p>Hello, <b>world</b>!</p>"
    # target_lang = "es"
    # translated_html = translate_html_markup(html_to_translate, target_lang)
    # print(f"Original HTML: {html_to_translate}")
    # print(f"Translated HTML ({target_lang}): {translated_html}")
    pass
