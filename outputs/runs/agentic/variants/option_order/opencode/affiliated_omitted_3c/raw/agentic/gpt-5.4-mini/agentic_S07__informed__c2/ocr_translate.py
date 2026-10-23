from typing import Any, Dict, List

from google.cloud import translate_v3


def translate_ocr_text(text: str, *, project_id: str, target_language_code: str, location: str = "global", source_language_code: str = None) -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    request = {
        "parent": parent,
        "contents": [text],
        "mime_type": "text/plain",
        "target_language_code": target_language_code,
    }
    if source_language_code:
        request["source_language_code"] = source_language_code
    response = client.translate_text(request=request)
    translations: List[str] = [item.translated_text for item in response.translations]
    return {"provider": "google-cloud-translate", "translations": translations, "raw": response}
