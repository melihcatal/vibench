import boto3
import os

comprehend_client = boto3.client("comprehend")

def document_field_extraction(text: str, language_code: str = "en") -> dict:
    response = comprehend_client.detect_entities(
        Text=text,
        LanguageCode=language_code,
    )
    entities = [
        {
            "text": entity["Text"],
            "type": entity["Type"],
            "score": entity["Score"],
        }
        for entity in response["Entities"]
    ]
    return {"entities": entities, "blocks": response["Blocks"] if "Blocks" in response else []}