import json

from deep_translator import GoogleTranslator


def translate_record(record, target_language="en"):
    translator = GoogleTranslator(source="auto", target=target_language)
    return {k: translator.translate(v) if isinstance(v, str) else v for k, v in record.items()}


def handler(event, context=None):
    record = event.get("record", event) if isinstance(event, dict) else event
    target_language = event.get("target_language", "en") if isinstance(event, dict) else "en"
    return {"statusCode": 200, "body": json.dumps({"ok": True, "record": translate_record(record, target_language)})}
