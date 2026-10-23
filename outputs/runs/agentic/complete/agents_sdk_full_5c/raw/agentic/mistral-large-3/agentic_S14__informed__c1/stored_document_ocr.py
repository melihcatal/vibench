import os
from typing import Dict, List

import boto3


def extract_text_from_document(bucket: str, key: str) -> Dict:
    """
    Run OCR on a document stored in Amazon S3 using Amazon Textract.
    """
    textract = boto3.client("textract", region_name=os.getenv("AWS_REGION", "us-east-1"))

    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )

    lines = [block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"]
    return {"text": "\n".join(lines)}