import os
from typing import Any, Dict, Union

from document_client import textract_client
from document_models import blocks_to_text


def extract_text(document: Union[str, bytes, Dict[str, Any]]) -> str:
    client = textract_client()
    if isinstance(document, bytes):
        response = client.detect_document_text(Document={"Bytes": document})
    elif isinstance(document, str) and document.startswith("s3://"):
        bucket_key = document[5:]
        bucket, key = bucket_key.split("/", 1)
        response = client.detect_document_text(Document={"S3Object": {"Bucket": bucket, "Name": key}})
    elif isinstance(document, str) and os.path.exists(document):
        with open(document, "rb") as handle:
            response = client.detect_document_text(Document={"Bytes": handle.read()})
    else:
        response = client.detect_document_text(Document=document)
    return blocks_to_text(response.get("Blocks", []))


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    text = extract_text(event["document"])
    return {"text": text}
