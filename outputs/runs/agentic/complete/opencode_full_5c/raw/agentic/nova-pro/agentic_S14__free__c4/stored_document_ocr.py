import boto3


def stored_document_ocr(bucket_name, object_name):
    client = boto3.client("textract")
    response = client.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": object_name}}
    )
    return response["Blocks"]
