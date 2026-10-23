from typing import Dict, Any
from document_client import DocumentClient
from document_models import OcrTranslation
from google.cloud import translate_v3 as translate

def ocr_translate(payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    project_id = config["project_id"]
    location = config["location"]
    target_language = config.get("target_language", "en")

    client = DocumentClient(project_id, location)
    translate_client = client.translate_client

    original_text = payload["text"]

    parent = f"projects/{project_id}/locations/{location}"

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [original_text],
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    source_language = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
        source_language = response.translations[0].detected_language_code

    return {"translation": OcrTranslation(
        original_text=original_text,
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language
    )}
