import boto3

from storage_client import storage_config


def stored_document_ocr(payload, config=None):
    cfg = storage_config(config)
    textract = boto3.client("textract", region_name=cfg.get("region"))
    return textract.analyze_document(
        Document={"S3Object": {"Bucket": cfg["bucket"], "Name": payload["object_name"]}},
        FeatureTypes=["FORMS", "TABLES"],
    )
