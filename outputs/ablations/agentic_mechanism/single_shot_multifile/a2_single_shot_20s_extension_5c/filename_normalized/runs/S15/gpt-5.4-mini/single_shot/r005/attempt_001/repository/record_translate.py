from typing import Any, Dict, List
import boto3

translate = boto3.client("translate")


def translate_records(payload: Dict[str, Any]) -> Dict[str, Any]:
    target_language = payload["target_language"]
    fields: List[str] = payload.get("fields", ["title", "description"])
    record = dict(payload.get("record", {}))
    output = dict(record)
    for field in fields:
        value = record.get(field)
        if isinstance(value, str) and value:
            result = translate.translate_text(Text=value[:5000], SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=target_language)
            output[field] = result.get("TranslatedText", value)
    return {"ok": True, "record": output}


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return translate_records(event)
