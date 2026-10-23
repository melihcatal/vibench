import json
import os
from typing import Any, Dict, List

import boto3

from database_models import normalize_document

COMPREHEND = boto3.client("comprehend", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))


def summarize_record(payload: Dict[str, Any]) -> Dict[str, Any]:
    record = normalize_document(payload.get("record", {}))
    text = " ".join(str(v) for v in record.values() if isinstance(v, (str, int, float)))[:4500]
    summary = text
    if text:
        resp = COMPREHEND.detect_dominant_language(Text=text)
        lang = resp.get("Languages", [{}])[0].get("LanguageCode", "en")
        summary = f"{lang}: {text[:240]}"
    return {"summary": summary, "record": record}


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if not sys.stdin.isatty() else os.environ.get("DOCUMENT_JSON", "{}")
    print(json.dumps(summarize_record(json.loads(raw or "{}"))))