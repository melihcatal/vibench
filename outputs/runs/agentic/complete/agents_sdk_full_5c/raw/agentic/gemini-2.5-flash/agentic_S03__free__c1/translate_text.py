from google.cloud import translate_v3
from translation_client import get_translation_client

def translate_single_text(text: str, target_language: str, source_language: str = None) -> str:
    """Translates a single piece of text using Google Cloud Translation."""
    client = get_translation_client()
    parent = f"projects/{client.project}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "source_language_code": source_language,
            "mime_type": "text/plain",
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # translated_text = translate_single_text("Hello World", "fr", "en")
    # print(f"Translated text: {translated_text}")
    pass
