import boto3
import os
from typing import List, Dict, Any
from document_models import normalize_ocr_text


def extract_text(image_path: str) -> str:
    client = boto3.client("textract", region_name=os.getenv("AWS_REGION", "us-east-1"))
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    response = client.detect_document_text(Document={"Bytes": image_bytes})
    blocks: List[Dict[str, Any]] = response["Blocks"]
    return normalize_ocr_text(blocks)
