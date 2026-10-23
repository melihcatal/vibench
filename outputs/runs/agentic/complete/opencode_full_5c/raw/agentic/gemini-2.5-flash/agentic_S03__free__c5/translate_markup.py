from translation_client import get_translation_client


def translate_markup(
    html_content: str, target_language: str, project_id: str, source_language: str = ""
) -> str:
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [html_content],
            "mime_type": "text/html",  # Specify HTML mime type
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    return response.translations[0].translated_text
