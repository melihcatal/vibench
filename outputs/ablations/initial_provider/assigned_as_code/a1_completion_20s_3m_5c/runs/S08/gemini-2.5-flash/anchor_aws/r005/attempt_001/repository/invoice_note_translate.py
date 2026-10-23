from typing import Dict, Any, Optional
from document_client import get_translate_client
import os

def translate_invoice_note(text: str, target_language_code: str = "en", source_language_code: Optional[str] = None, config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = config.get("gcp_location", os.environ.get("GCP_LOCATION", "global"))

    client = get_translate_client(location=location)

    parent = f"projects/{project_id}/locations/{location}"

    if source_language_code:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
                "source_language_code": source_language_code,
            }
        )
    else:
        # Let the API detect the source language
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
            }
        )

    translated_text = ""
    detected_language = ""

    for translation in response.translations:
        translated_text = translation.translated_text
        detected_language = translation.detected_language_code
        break # Assuming only one text for translation

    return {"translated_text": translated_text, "detected_language_code": detected_language}
