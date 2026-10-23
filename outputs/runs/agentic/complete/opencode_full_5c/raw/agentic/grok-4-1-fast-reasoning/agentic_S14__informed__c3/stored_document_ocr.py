import boto3
from storage_client import download_bytes
from botocore.exceptions import ClientError


def ocr_document(key: str) -> str:
    data = download_bytes(key)
    textract = boto3.client("textract")
    response = textract.detect_document_text(Document={"Bytes": data})
    text_parts = [
        block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"
    ]
    return "\n".join(text_parts).strip()
