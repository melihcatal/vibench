from translation_client import get_translation_client


def translate_text(
    text: str, target_language: str, project_id: str, source_language: str = ""
) -> str:
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Use "text/html" for HTML input
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    # Assuming only one text input for single translation
    return response.translations[0].translated_text
