import boto3

from database_models import normalize_item


def record_translate(record, source_language="en", target_language="es"):
    translate = boto3.client("translate", region_name="us-east-1")
    item = normalize_item(record) or {}
    text = str(item.get("title") or item.get("content") or "")
    if not text:
        return {"translated": item}
    response = translate.translate_text(Text=text[:5000], SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    item["translated_text"] = response.get("TranslatedText")
    return item
