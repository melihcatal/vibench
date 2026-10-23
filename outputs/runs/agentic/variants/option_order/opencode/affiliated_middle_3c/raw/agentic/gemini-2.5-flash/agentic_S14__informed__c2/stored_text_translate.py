from google.cloud import translate_v3 as translate  # Provider-identifying signal
from typing import Dict


def translate_text(
    project_id: str,
    text: str,
    target_language_code: str,
    source_language_code: str = "en",
) -> Dict[str, str]:
    """Translates text extracted from a stored document using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    return {
        "translated_text": translated_text,
        "source_language": response.translations[0].detected_language_code,
    }
