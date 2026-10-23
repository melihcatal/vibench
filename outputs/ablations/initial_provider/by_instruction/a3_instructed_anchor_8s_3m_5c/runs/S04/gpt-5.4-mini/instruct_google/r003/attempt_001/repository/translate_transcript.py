from typing import Any, Dict, List

from google.cloud import translate_v3 as translate


def translate_segments(segments: List[Dict[str, Any]], target_language: str = "es") -> Dict[str, Any]:
    client = translate.TranslationServiceClient()
    parent = client.location_path("PROJECT_ID", "global")
    contents = [str(segment.get("text", "")) for segment in segments]
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": contents,
            "target_language_code": target_language,
            "mime_type": "text/plain",
        }
    )
    return {"provider": "google", "translations": [item.translated_text for item in response.translations]}
