import boto3


def stored_document_ocr(bucket_name, object_key):
    textract = boto3.client("textract")
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}
    )
    print(f"OCR results for {object_key}: {response}")
    return response
