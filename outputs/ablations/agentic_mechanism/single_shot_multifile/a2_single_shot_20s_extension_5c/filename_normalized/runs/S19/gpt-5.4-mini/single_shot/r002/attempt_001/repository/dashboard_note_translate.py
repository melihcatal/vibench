import os
from typing import Dict

import boto3


def dashboard_note_translate(text: str, target_locale: str) -> Dict[str, str]:
    translate = boto3.client("translate", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    resp = translate.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_locale)
    return {"source_text": text, "target_locale": target_locale, "translated_text": resp.get("TranslatedText", "")}
