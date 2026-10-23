import json
from typing import Any, Dict

import boto3

from security_models import normalize_text


def translate_compliance_note(text: str, target_language_code: str = "es") -> Dict[str, Any]:
    client = boto3.client("translate")
    source_text = normalize_text(text)
    response = client.translate_text(Text=source_text, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)
    return {"provider": "aws-translate", "source_text": source_text, "translated_text": response.get("TranslatedText", ""), "target_language_code": target_language_code}
