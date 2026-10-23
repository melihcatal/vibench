import boto3


def ocr_stored_document(bucket: str, key: str) -> str:
    textract = boto3.client("textract", region_name="us-east-1")
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    text = []
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            text.append(block["Text"])
    return "\n".join(text)
