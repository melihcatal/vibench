from typing import Any, Dict

from google.cloud import translate_v3 as translate

from vision_client import load_vision_config


def alt_text_translate(text: str, target_language_code: str = "es") -> Dict[str, Any]:
    cfg = load_vision_config()
    client = translate.TranslationServiceClient()
    parent = client.common_location_path(cfg.get("project_id") or "", "global")
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    translations = [item.translated_text for item in response.translations]
    return {"provider": "google_cloud_translate_v3", "target_language_code": target_language_code, "translations": translations}
