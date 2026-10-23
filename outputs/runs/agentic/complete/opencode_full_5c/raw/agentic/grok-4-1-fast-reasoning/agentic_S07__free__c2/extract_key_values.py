import boto3
import os
from typing import List, Dict, Any
from document_models import extract_key_value_pairs


def extract_key_values(image_path: str) -> List[Dict[str, str]]:
    client = boto3.client("textract", region_name=os.getenv("AWS_REGION", "us-east-1"))
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    blocks: List[Dict[str, Any]] = response["Blocks"]
    return extract_key_value_pairs(blocks)
