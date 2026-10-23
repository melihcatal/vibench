from typing import Dict, List

import boto3

from document_models import OcrResult


def extract_structured_fields(result: OcrResult, fields: List[str]) -> Dict[str, str]:
    client = boto3.client("comprehend")
    response = client.detect_entities(Text=result.text[:4500], LanguageCode="en")
    entities = response.get("Entities", [])
    extracted: Dict[str, str] = {}
    for field in fields:
        for entity in entities:
            if entity.get("Type", "").lower() == field.lower():
                extracted[field] = entity.get("Text", "")
                break
    return extracted
