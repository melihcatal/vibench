import os
from typing import Dict

import boto3
from botocore.exceptions import ClientError


class TextractOCRClient:
    def __init__(self):
        self.textract_client = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def run_ocr_on_stored_document(self, bucket_name: str, object_key: str) -> Dict:
        try:
            response = self.textract_client.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
            )
            return {
                "text": "\n".join(
                    [
                        item["Text"]
                        for item in response.get("Blocks", [])
                        if item["BlockType"] == "LINE"
                    ]
                ),
                "metadata": {"bucket": bucket_name, "key": object_key},
            }
        except ClientError as e:
            raise Exception(f"Failed to run OCR: {e}")
