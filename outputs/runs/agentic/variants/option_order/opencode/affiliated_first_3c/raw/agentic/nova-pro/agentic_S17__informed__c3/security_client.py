import boto3


def get_kms_client():
    return boto3.client("kms")


def normalize_payload(payload):
    return payload.encode("utf-8")
