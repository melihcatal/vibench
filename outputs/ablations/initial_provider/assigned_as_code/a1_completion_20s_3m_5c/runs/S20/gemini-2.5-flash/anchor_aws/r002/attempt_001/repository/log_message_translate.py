from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import TranslationRequest

def translate_log_message(text_content: str, target_language: str, project_id: str, location: str) -> Dict[str, Any]:
    client = ObservabilityClient(region_name="us-east-1", project_id=project_id, location=location)
    translate_client = client.get_translate_client()

    parent = f"projects/{project_id}/locations/{location}"
    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)

    return {"original_text": text_content, "translated_text": translations[0] if translations else ""}
