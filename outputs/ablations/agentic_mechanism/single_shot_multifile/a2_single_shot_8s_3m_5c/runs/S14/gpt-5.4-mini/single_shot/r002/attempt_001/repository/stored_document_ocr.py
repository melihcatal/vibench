import os
from typing import Optional

import boto3
from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import StoredDocumentOCRRequest, StoredDocumentOCRResponse

AWS_TEXTRACT_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def run_stored_document_ocr(request: StoredDocumentOCRRequest) -> StoredDocumentOCRResponse:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    key = resolve_object_key(request.key)
    obj = s3.get_object(Bucket=bucket, Key=key)
    textract = boto3.client("textract", region_name=AWS_TEXTRACT_REGION)
    document = {"Bytes": obj["Body"].read()}
    resp = textract.detect_document_text(Document=document)
    lines = [b["Text"] for b in resp.get("Blocks", []) if b.get("BlockType") == "LINE" and b.get("Text")]
    return StoredDocumentOCRResponse(bucket=bucket, key=key, text="\n".join(lines), page_count=1, provider="aws-textract")
