import boto3
import os


def stored_document_ocr(payload, config=None):
    config = config or {}
    textract_client = boto3.client("textract", region_name=config.get("region") or os.environ.get("AWS_REGION"))
    s3_object_name = payload["object_name"]

    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': config["bucket"],
                'Name': s3_object_name
            }
        }
    )

    extracted_text = []
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            extracted_text.append(item["Text"])

    return {"object_name": s3_object_name, "extracted_text": "\n".join(extracted_text)}
