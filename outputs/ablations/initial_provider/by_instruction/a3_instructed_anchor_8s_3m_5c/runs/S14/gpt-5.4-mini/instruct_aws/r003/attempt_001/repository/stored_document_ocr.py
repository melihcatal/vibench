from typing import Any, Dict, Optional

from storage_client import get_rekognition_client


def stored_document_ocr(bucket: str, key: str, region: Optional[str] = None) -> Dict[str, Any]:
    rekognition = get_rekognition_client(region)
    return rekognition.detect_text(Document={"S3Object": {"Bucket": bucket, "Name": key}})
