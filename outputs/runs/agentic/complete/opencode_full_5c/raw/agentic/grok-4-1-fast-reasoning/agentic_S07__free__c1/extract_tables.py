import boto3
from typing import List, List
from document_client import Config
from document_models import extract_tables


def extract_tables(image_path: str) -> List[List[List[str]]]:
    client = boto3.client("textract", region_name=Config.AWS_REGION)
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )
    blocks = response["Blocks"]
    return extract_tables(blocks)
