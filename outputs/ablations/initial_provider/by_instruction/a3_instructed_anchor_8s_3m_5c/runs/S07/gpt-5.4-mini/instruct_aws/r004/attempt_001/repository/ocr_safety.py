from typing import Any, Dict

import boto3

from extract_text import extract_text


def check_ocr_safety(document: Any) -> Dict[str, Any]:
    text = extract_text(document).text
    client = boto3.client("comprehend")
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    return {"text": text, "pii_entities": response.get("Entities", [])}
