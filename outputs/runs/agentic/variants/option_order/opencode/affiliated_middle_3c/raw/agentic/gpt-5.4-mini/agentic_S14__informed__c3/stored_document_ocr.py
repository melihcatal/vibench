import boto3


def run_stored_document_ocr(bucket: str, key: str, region_name: str | None = None):
    client = boto3.client("textract", region_name=region_name)
    return client.analyze_document(
        Document={"S3Object": {"Bucket": bucket, "Name": key}},
        FeatureTypes=["FORMS", "TABLES"],
    )
