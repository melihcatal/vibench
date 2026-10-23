import boto3

from storage_client import get_bucket_name, load_storage_config
from storage_models import normalize_object_name


def stored_document_ocr(payload, config=None):
    config = load_storage_config(config)
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={"S3Object": {"Bucket": get_bucket_name(config), "Name": normalize_object_name(payload["object_name"]) }}, FeatureTypes=["FORMS", "TABLES"])
    return {"blocks": response.get("Blocks", [])}
