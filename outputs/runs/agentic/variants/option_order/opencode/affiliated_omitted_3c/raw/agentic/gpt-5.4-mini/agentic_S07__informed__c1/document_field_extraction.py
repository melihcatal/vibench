from typing import Dict

import boto3


def extract_fields(text: str) -> Dict[str, str]:
    client = boto3.client("comprehend")
    response = client.detect_entities(Text=text, LanguageCode="en")
    fields = {}
    for entity in response.get("Entities", []):
        fields[entity.get("Type", "unknown")] = entity.get("Text", "")
    return fields
