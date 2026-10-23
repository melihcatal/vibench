import json
from google.cloud import translate_v2 as translate
from messaging_models import MessageEvent

translate_client = translate.Client()


def translate_message_payload(event: MessageEvent, target_language: str = "es") -> str:
    payload_str = json.dumps(event.payload)
    result = translate_client.translate(payload_str, target_language=target_language)
    return result["translatedText"]
