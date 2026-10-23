import boto3
import os
from typing import List, Dict, Any
from document_models import normalize_layout_elements


def extract_layout(image_path: str) -> List[Dict[str, Any]]:
    client = boto3.client("textract", region_name=os.getenv("AWS_REGION", "us-east-1"))
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["LAYOUT"]
    )
    blocks: List[Dict[str, Any]] = response["Blocks"]
    return normalize_layout_elements(blocks)
