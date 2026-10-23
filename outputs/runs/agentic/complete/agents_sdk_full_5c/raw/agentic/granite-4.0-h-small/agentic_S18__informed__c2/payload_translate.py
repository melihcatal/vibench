import os
import requests
from messaging_models import PubSubMessage, ProcessingResult
from messaging_client import PubSubClient

def translate_text(text: str, target_lang: str = "es") -> str:
    """Translate a string using DeepL API (requires DEEPL_AUTH_KEY env var)."""
    deepl_key = os.getenv("DEEPL_AUTH_KEY")
    if not deepl_key:
        raise RuntimeError("Missing DEEPL_AUTH_KEY environment variable")
    endpoint = "https://api.deepl.com/v2/translate"
    params = {"text": text, "target_lang": target_lang, "preserve_formatting": 1}
    headers = {"Authorization": f"DeepL-Auth-Key {deepl_key}"}
    resp = requests.post(endpoint, params=params, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"DeepL error {resp.status_code}: {resp.text}")
    translations = resp.json().get("translations", [])
    if not translations:
        raise RuntimeError("Unexpected DeepL response")
    return translations[0].get("text", text)

def translate_message(original_msg: PubSubMessage, target_lang: str = "es") -> ProcessingResult:
    """Translate the 'body' field of a message payload to a target language.

    Returns a ProcessingResult with the translated payload attached if successful.
    """
    payload = json.loads(original_msg.data)
    original_body = payload.get("body", "")
    if not original_body:
        return build_processing_result(original_msg.message_id, "failed", "missing_body")
    try:
        translated_body = translate_text(original_body, target_lang)
    except Exception as exc:
        return build_processing_result(original_msg.message_id, "failed", str(exc))
    # Build enriched payload
    new_payload = payload.copy()
    new_payload["translated_body"] = translated_body
    new_payload["translation_lang"] = target_lang
    enriched_msg = PubSubMessage(
        data=json.dumps(new_payload).encode("utf-8"),
        attributes=original_msg.attributes,
    )
    # Publish to a designated translation topic
    translator = PubSubClient()
    topic = os.getenv("TRANSLATION_PUBLISH_TOPIC")
    if not topic:
        raise RuntimeError("TRANSLATION_PUBLISH_TOPIC env var not set")
    future = translator.publish(topic, enriched_msg)
    future.result()  # wait for ack
    return build_processing_result(original_msg.message_id, "ok", transformed_payload=new_payload)

if __name__ == "__main__":
    # Demo (requires DEEPL_AUTH_KEY and TRANSLATION_PUBLISH_TOPIC env vars)
    translate_message(PubSubMessage(data=b"{\"body\":\"Hello world\"}"), target_lang="es")
