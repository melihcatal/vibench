import boto3
from storage_client import get_storage_config
from storage_models import normalize_key


def stored_document_ocr(payload, config=None):
    config = get_storage_config(config)
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.start_document_text_detection(DocumentLocation={"S3Object": {"Bucket": config["bucket"], "Name": normalize_key(payload)}})
    return {"job_id": response["JobId"], "object_name": normalize_key(payload)}
