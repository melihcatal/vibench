from typing import Any, Dict

import boto3

from extract_text import extract_text


def extract_document_fields(document: Any, model_arn: str) -> Dict[str, Any]:
    text = extract_text(document).text
    client = boto3.client("comprehendmedical")
    response = client.detect_entities_v2(Text=text)
    return {"text": text, "entities": response.get("Entities", []), "model_arn": model_arn}
