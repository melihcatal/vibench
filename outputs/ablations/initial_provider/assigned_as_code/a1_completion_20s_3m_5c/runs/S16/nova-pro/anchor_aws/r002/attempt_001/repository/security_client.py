import boto3

def get_client(region):
    return boto3.client("secretsmanager", region_name=region)

def normalize_payload(payload):
    return {"secret_id": payload.get("secret_id"), "key_field": payload.get("key_field")}