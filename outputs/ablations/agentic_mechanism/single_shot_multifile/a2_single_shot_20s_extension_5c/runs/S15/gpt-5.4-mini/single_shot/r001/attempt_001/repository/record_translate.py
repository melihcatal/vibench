import json
import os
from typing import Any, Dict

import boto3

TRANSLATOR = boto3.client("translate", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))


def translate_record(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text", payload.get("record", {})))
    source = payload.get("source_language_code", "auto")
    target = payload.get("target_language_code", "en")
    if source == "auto":
        detection = TRANSLATOR.translate_text(Text=text[:5000], SourceLanguageCode="auto", TargetLanguageCode=target)
    else:
        detection = TRANSLATOR.translate_text(Text=text[:5000], SourceLanguageCode=source, TargetLanguageCode=target)
    return {"translated_text": detection.get("TranslatedText", text), "source_language_code": source, "target_language_code": target}


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if not sys.stdin.isatty() else os.environ.get("DOCUMENT_JSON", "{}")
    print(json.dumps(translate_record(json.loads(raw or "{}"))))