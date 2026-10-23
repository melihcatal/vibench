import json
from typing import Any, Dict

import boto3


def check_ocr_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("comprehend")
    text = payload.get("text", "")
    response = client.detect_pii_entities(Text=text, LanguageCode=payload.get("language_code", "en"))
    return {"entities": response.get("Entities", []), "raw": response}


if __name__ == "__main__":
    import sys

    print(json.dumps(check_ocr_safety(json.loads(sys.stdin.read())), ensure_ascii=False))
