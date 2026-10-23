import os
import boto3
from typing import List, Dict, TypedDict


class Field(TypedDict):
    type: str
    text: str
    score: float
    start: int
    end: int


def document_field_extraction(text: str) -> List[Field]:
    client = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    response = client.detect_entities(Text=text, LanguageCode="en")
    fields = []
    for entity in response.get("Entities", []):
        fields.append(
            {
                "type": entity["Type"],
                "text": entity["Text"],
                "score": entity["Score"],
                "start": entity["BeginOffset"],
                "end": entity["EndOffset"],
            }
        )
    return fields
