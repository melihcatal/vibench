import boto3


def stored_document_ocr(bucket_name, object_key):
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
        FeatureTypes=["TABLES", "FORMS"],
    )
    return response
