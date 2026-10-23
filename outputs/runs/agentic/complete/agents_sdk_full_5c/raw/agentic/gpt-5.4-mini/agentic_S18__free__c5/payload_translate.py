import json
import sys
from typing import Any, Dict

from google.cloud import translate_v3 as translate

from messaging_models import TranslationRequest


client = translate.TranslationServiceClient()


def translate_payload(message: Dict[str, Any], target_language: str = "es") -> Dict[str, Any]:
    text = str(message.get("text") or message.get("payload") or "")
    request = TranslationRequest(message_id=str(message.get("message_id") or message.get("id") or "unknown"), text=text, target_language=target_language)
    parent = client.common_location_path("demo-project", "global")
    response = client.translate_text(request={"parent": parent, "contents": [request.text], "mime_type": "text/plain", "target_language_code": request.target_language})
    translated = response.translations[0].translated_text if response.translations else text
    return {"message_id": request.message_id, "translated_text": translated, "target_language": request.target_language, "provider": "google-cloud-translate-v3"}


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "{}"
    message = json.loads(raw)
    print(json.dumps(translate_payload(message), ensure_ascii=False))
