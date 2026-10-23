from typing import Dict
from storage_client import StorageClient
import requests


def stored_document_ocr(bucket_name: str, object_key: str) -> str:
    """
    Runs OCR on a document stored in Amazon S3 using AWS Textract.
    """
    client = StorageClient().get_client()

    try:
        # Fetch the object from S3
        response = client.get_object(Bucket=bucket_name, Key=object_key)
        document_bytes = response["Body"].read()

        # Call AWS Textract for OCR
        textract_client = client("textract", region_name="us-east-1")
        textract_response = textract_client.detect_document_text(
            Document={"Bytes": document_bytes}
        )

        # Extract text from Textract response
        text = "".join(
            [
                item["Text"]
                for item in textract_response["Blocks"]
                if item["BlockType"] == "LINE"
            ]
        )

        return text
    except Exception as e:
        raise Exception(f"Failed to perform OCR on S3 document: {str(e)}")
