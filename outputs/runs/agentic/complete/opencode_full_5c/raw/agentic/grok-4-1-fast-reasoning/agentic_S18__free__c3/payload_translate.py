import os
import json
import requests
from messaging_models import PubSubMessage


def translate_payload(message: PubSubMessage, target_lang: str = "ES") -> PubSubMessage:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return message
    payload = message.payload
    text = payload.get("text", json.dumps(payload))
    if not text:
        return message
    url = "https://api-free.deepl.com/v2/translate"
    params = {"auth_key": auth_key, "text": text, "target_lang": target_lang}
    try:
        resp = requests.post(url, data=params)
        resp.raise_for_status()
        result = resp.json()
        translated_text = result["translations"][0]["text"]
        new_payload = payload.copy()
        new_payload["text_translated"] = translated_text
        new_data = json.dumps(new_payload).encode("utf-8")
        return PubSubMessage(
            message_id=message.message_id,
            data=new_data,
            attributes=message.attributes,
            publish_time=message.publish_time,
        )
    except Exception:
        return message
