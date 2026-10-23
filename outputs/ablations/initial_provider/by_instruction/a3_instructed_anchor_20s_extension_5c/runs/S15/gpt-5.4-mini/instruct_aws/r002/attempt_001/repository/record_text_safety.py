import json

import boto3


def record_text_safety(document):
    client = boto3.client("comprehend")
    text = json.dumps(document, ensure_ascii=False)
    response = client.detect_pii_entities(Text=text[:4500], LanguageCode="en")
    return {"unsafe": bool(response.get("Entities")), "entities": response.get("Entities", [])}
