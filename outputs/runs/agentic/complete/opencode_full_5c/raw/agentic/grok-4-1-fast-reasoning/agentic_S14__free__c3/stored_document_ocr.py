import boto3


def stored_document_ocr(bucket: str, key: str) -> str:
    textract = boto3.client("textract")
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    text = ""
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            text += block.get("Text", "") + "\n"
    return text.strip()
