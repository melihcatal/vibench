from translation_client import get_translation_client


def quality_summary(
    original_text: str,
    translated_text: str,
    target_language: str,
    project_id: str,
    source_language: str = "",
) -> str:
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    # For a basic quality check, we can back-translate and compare lengths or simple metrics.
    # A more sophisticated approach would involve NLP metrics or human evaluation.
    # Here, we'll do a simple back-translation to see if the translated text is roughly equivalent.

    back_translated_response = client.translate_text(
        request={
            "parent": parent,
            "contents": [translated_text],
            "mime_type": "text/plain",
            "source_language_code": target_language,
            "target_language_code": source_language,
        }
    )
    back_translated_text = back_translated_response.translations[0].translated_text

    # Simple comparison for demonstration purposes
    if (
        len(original_text) * 0.8
        <= len(back_translated_text)
        <= len(original_text) * 1.2
    ):
        return f"Translation appears to be of reasonable length after back-translation. Original: '{original_text}', Translated: '{translated_text}', Back-translated: '{back_translated_text}'"
    else:
        return f"Translation length deviates significantly after back-translation. Original: '{original_text}', Translated: '{translated_text}', Back-translated: '{back_translated_text}'"
