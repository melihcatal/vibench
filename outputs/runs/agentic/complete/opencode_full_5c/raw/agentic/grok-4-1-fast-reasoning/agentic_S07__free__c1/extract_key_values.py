import boto3
from typing import Dict, List, Any
from document_client import Config
from document_models import extract_key_value_pairs


def extract_key_values(image_path: str) -> Dict[str, str]:
    client = boto3.client("textract", region_name=Config.AWS_REGION)
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    blocks: List[Dict[str, Any]] = response["Blocks"]
    return extract_key_value_pairs(blocks)
