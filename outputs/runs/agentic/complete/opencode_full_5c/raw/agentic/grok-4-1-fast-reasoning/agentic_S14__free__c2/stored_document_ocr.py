import boto3


def stored_document_ocr(bucket: str, key: str) -> str:
    client = boto3.client("textract")
    response = client.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    text_parts = [
        block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"
    ]
    return "\n".join(text_parts)
