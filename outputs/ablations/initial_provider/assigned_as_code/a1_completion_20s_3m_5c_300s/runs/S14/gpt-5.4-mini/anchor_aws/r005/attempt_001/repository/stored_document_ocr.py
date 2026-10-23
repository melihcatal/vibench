import boto3

from storage_client import load_storage_config
from storage_models import normalize_object_name


def stored_document_ocr(payload, config=None):
    config = load_storage_config(config)
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": config["bucket"], "Name": normalize_object_name(payload["object_name"])}}
    )
    return {"job_id": response["JobId"]}
