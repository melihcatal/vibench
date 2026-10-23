import boto3


def stored_document_ocr(bucket: str, key: str, region: str | None = None) -> dict:
    textract = boto3.client("textract", region_name=region)
    return textract.analyze_document(
        Document={"S3Object": {"Bucket": bucket, "Name": key}},
        FeatureTypes=["FORMS", "TABLES"],
    )
