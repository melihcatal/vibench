from typing import Any, Dict

from google.cloud import translate_v3


def invoice_note_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    client = translate_v3.TranslationServiceClient()
    response = client.translate_text(
        request={
            "parent": "projects/sample/locations/global",
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return {"provider": "google_cloud_translate_v3", "response": response}
