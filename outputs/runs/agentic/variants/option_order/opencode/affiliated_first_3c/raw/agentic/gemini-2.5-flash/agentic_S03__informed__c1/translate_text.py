from translation_client import get_translation_client


def translate_text(
    text: str, target_language_code: str, source_language_code: str = "en"
) -> str:
    """Translates a single text string using Google Cloud Translation."""
    client = get_translation_client()
    project_id = ""  # Replace with your Google Cloud Project ID
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
