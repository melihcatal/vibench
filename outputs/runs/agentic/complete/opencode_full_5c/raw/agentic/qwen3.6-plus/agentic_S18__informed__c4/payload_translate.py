import os
import json
import deepl
from messaging_models import PubSubEvent, ConsumeResult


def translate_payload(
    result: ConsumeResult,
    target_language: str = "EN",
    source_language: str | None = None,
) -> dict:
    event = result.to_event()
    if event is None:
        return {"error": "No valid event to translate", "translated_payload": None}

    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)

    text_fields = {}
    for key, value in event.payload.items():
        if isinstance(value, str) and len(value.strip()) > 0:
            text_fields[key] = value

    if not text_fields:
        return {
            "event_id": event.event_id,
            "message_id": result.message_id,
            "translated_payload": event.payload,
            "target_language": target_language,
            "source_language": "none",
            "service": "DeepL API",
        }

    translated_payload = dict(event.payload)
    translation_details = {}

    for key, text in text_fields.items():
        translate_kwargs = {"target_lang": target_language}
        if source_language:
            translate_kwargs["source_lang"] = source_language

        translation_result = translator.translate_text(text, **translate_kwargs)
        translated_payload[key] = translation_result.text
        translation_details[key] = {
            "detected_source": translation_result.detected_source_lang,
            "original": text,
            "translated": translation_result.text,
        }

    return {
        "event_id": event.event_id,
        "message_id": result.message_id,
        "translated_payload": translated_payload,
        "target_language": target_language,
        "translation_details": translation_details,
        "service": "DeepL API",
    }


if __name__ == "__main__":
    evt = PubSubEvent(
        event_type="user.message",
        source="chat-service",
        payload={"greeting": "Hola, como estas?", "subject": "Consulta"},
    )
    cr = ConsumeResult(message_id="msg-translate-001", event=evt)
    translation = translate_payload(cr, target_language="EN-US")
    print(json.dumps(translation, indent=2))
