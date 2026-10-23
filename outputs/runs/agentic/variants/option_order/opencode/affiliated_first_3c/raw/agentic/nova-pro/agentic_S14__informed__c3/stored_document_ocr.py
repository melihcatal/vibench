import boto3


def stored_document_ocr(bucket_name, object_key):
    textract = boto3.client("textract")
    response = textract.start_document_text_detection(
        Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
    )
    return response["JobId"]
