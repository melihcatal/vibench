import boto3
from typing import List, Dict, Any
from document_client import Config
from document_models import extract_layout_elements


def extract_layout(image_path: str) -> List[Dict[str, Any]]:
    client = boto3.client("textract", region_name=Config.AWS_REGION)
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["LAYOUTS"]
    )
    blocks: List[Dict[str, Any]] = response["Blocks"]
    return extract_layout_elements(blocks)
