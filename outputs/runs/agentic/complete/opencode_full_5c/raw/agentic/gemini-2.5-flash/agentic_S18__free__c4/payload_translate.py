from google.cloud import translate


def translate_payload_text(
    text: str, target_language_code: str, project_id: str
) -> dict:
    """Translates customer-facing message payload text using Google Cloud Translation API.

    Args:
        text: The text content to translate.
        target_language_code: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id: Your Google Cloud Project ID.

    Returns:
        A dictionary containing the original text, translated text, and detected source language.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(
            {
                "translated_text": translation.translated_text,
                "detected_language_code": translation.detected_language_code,
            }
        )

    if translations:
        return {
            "original_text": text,
            "translated_text": translations[0]["translated_text"],
            "detected_source_language": translations[0]["detected_language_code"],
            "provider": "Google Cloud Translation API v3",
        }
    return {
        "original_text": text,
        "translated_text": text,
        "detected_source_language": "N/A",
        "provider": "Google Cloud Translation API v3",
    }
