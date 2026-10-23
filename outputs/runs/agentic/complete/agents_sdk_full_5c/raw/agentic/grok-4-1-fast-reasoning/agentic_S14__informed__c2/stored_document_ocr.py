import boto3
from storage_client import get_bucket_name

def stored_document_ocr(
    bucket_name: str | None = None,
    key: str
) -> dict:
    if bucket_name is None:
        bucket_name = get_bucket_name()
    textract_client = boto3.client("textract", region_name="us-east-1")
    response = textract_client.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": key}}
    )
    extracted_text = ""
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            extracted_text += block["Text"] + "\n"
    return {
        "extracted_text": extracted_text.strip(),
        "confidence": [b.get("Confidence", 0) for b in response["Blocks"] if b["BlockType"] == "LINE"],
        "blocks": response["Blocks"][:10]  # first 10 for brevity
    }
