import json
import os
from typing import Any, Dict

import boto3

CONTENT_MODERATION = boto3.client("comprehend", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))


def check_text_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text", payload.get("record", {})))
    response = CONTENT_MODERATION.detect_dominant_language(Text=text[:5000])
    language = response.get("Languages", [{}])[0].get("LanguageCode", "en")
    unsafe = any(token in text.lower() for token in ["violence", "hate", "self-harm", "abuse"])
    return {"language": language, "unsafe": unsafe, "text": text}


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if not sys.stdin.isatty() else os.environ.get("DOCUMENT_JSON", "{}")
    print(json.dumps(check_text_safety(json.loads(raw or "{}"))))