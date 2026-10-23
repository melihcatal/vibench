import boto3
from typing import Dict, Any, List
from storage_client import get_aws_client_kwargs


def ocr_stored_document(bucket: str, object_key: str) -> Dict[str, Any]:
    kwargs = get_aws_client_kwargs()
    textract_client = boto3.client("textract", **kwargs)
    response = textract_client.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": object_key}}
    )
    text = ""
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            text += block["Text"] + "\\n"
    return {"extracted_text": text.strip(), "blocks": response["Blocks"]}
