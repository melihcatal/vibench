from google.cloud import translate_v3
from translation_client import get_translation_client

def translate_html_markup(html_content: str, target_language: str, source_language: str = None) -> str:
    """Translates HTML content using Google Cloud Translation, preserving tags."""
    client = get_translation_client()
    parent = f"projects/{client.project}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [html_content],
            "target_language_code": target_language,
            "source_language_code": source_language,
            "mime_type": "text/html", # Specify HTML content type
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # html = "<p>Hello <b>World</b>!</p>"
    # translated_html = translate_html_markup(html, "fr", "en")
    # print(f"Translated HTML: {translated_html}")
    pass
