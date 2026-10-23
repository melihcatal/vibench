import boto3
import os
from typing import List
from document_models import parse_tables


def extract_tables(image_path: str) -> List[List[List[str]]]:
    client = boto3.client("textract", region_name=os.getenv("AWS_REGION", "us-east-1"))
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )
    blocks = response["Blocks"]
    return parse_tables(blocks)
