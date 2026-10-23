import boto3

from storage_client import get_s3_client
from storage_models import OCRResponse, StorageObjectRef


def stored_document_ocr(ref: StorageObjectRef) -> OCRResponse:
    s3 = get_s3_client()
    textract = boto3.client("textract")
    document = s3.get_object(Bucket=ref.bucket, Key=ref.key)
    result = textract.detect_document_text(Document={"Bytes": document["Body"].read()})
    lines = [block.get("Text", "") for block in result.get("Blocks", []) if block.get("BlockType") == "LINE" and block.get("Text")]
    return OCRResponse(bucket=ref.bucket, key=ref.key, text="\n".join(lines))
