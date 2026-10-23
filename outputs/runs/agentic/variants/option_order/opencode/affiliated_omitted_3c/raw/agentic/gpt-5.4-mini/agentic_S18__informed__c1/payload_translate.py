from typing import Dict

import boto3


def translate_payload_text(text: str, source_lang: str = "auto", target_lang: str = "en") -> Dict[str, Any]:
    client = boto3.client("translate")
    response = client.translate_text(Text=text, SourceLanguageCode=source_lang if source_lang != "auto" else "auto", TargetLanguageCode=target_lang)
    return {"provider": "amazon-translate", "translated_text": response.get("TranslatedText"), "source_language": response.get("SourceLanguageCode"), "target_language": response.get("TargetLanguageCode")}
