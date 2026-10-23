import json

import boto3


def record_translate(document, target_language_code="es"):
    client = boto3.client("translate")
    text = json.dumps(document, ensure_ascii=False)
    response = client.translate_text(Text=text[:5000], SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return {"translated_text": response.get("TranslatedText"), "target_language_code": target_language_code}
