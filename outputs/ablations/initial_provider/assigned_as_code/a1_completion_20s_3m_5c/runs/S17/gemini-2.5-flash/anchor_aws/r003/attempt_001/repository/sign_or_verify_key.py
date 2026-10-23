import boto3
import base64
from botocore.exceptions import ClientError

def sign_payload(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    try:
        response = client.sign(
            KeyId=config["key_id"],
            Message=payload["message"],
            MessageType="RAW",
            SigningAlgorithm=config.get("signing_algorithm", "RSASSA_PKCS1_V1_5_SHA256")
        )
        return {"signature": response["Signature"]}
    except ClientError as e:
        return {"error": str(e)}

def verify_signature(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    try:
        response = client.verify(
            KeyId=config["key_id"],
            Message=payload["message"],
            MessageType="RAW",
            Signature=payload["signature"],
            SigningAlgorithm=config.get("signing_algorithm", "RSASSA_PKCS1_V1_5_SHA256")
        )
        return {"signature_valid": response["SignatureValid"]}
    except ClientError as e:
        return {"error": str(e), "signature_valid": False}