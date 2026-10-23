import os
import boto3
from botocore.config import Config


def get_kms_client():
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        region_name=region,
    )
    return boto3.client(
        "kms",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=region,
        config=config,
    )


def get_bedrock_client():
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        region_name=region,
    )
    return boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=region,
        config=config,
    )


def get_comprehend_client():
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        region_name=region,
    )
    return boto3.client(
        "comprehend",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=region,
        config=config,
    )


def get_translate_client():
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        region_name=region,
    )
    return boto3.client(
        "translate",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=region,
        config=config,
    )


def validate_key_id(key_id):
    if not key_id:
        raise ValueError(
            "Key ID is required. Set AWS_KMS_KEY_ID environment variable or pass key_id."
        )
    if not isinstance(key_id, str) or len(key_id.strip()) == 0:
        raise ValueError("Key ID must be a non-empty string.")


def generate_data_key(client, key_id, encryption_context=None):
    import base64

    kwargs = {"KeyId": key_id, "KeySpec": "AES_256"}
    if encryption_context:
        kwargs["EncryptionContext"] = encryption_context
    response = client.generate_data_key(**kwargs)
    return {
        "plaintext_key": base64.b64encode(response["Plaintext"]).decode("utf-8"),
        "encrypted_key": base64.b64encode(response["CiphertextBlob"]).decode("utf-8"),
        "key_id": response["KeyId"],
    }


def load_config():
    return {
        "aws_region": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        "kms_key_id": os.environ.get("AWS_KMS_KEY_ID", ""),
        "signing_key_id": os.environ.get("AWS_KMS_SIGNING_KEY_ID", ""),
        "encryption_context": {},
    }
