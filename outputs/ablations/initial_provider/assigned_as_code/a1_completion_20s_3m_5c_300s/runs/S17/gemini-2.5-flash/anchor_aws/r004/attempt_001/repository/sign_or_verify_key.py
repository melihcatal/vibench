import boto3
import base64


def sign_payload(payload, config=None):
    config = config or {}
    kms_client = boto3.client("kms", region_name=config.get("region"))

    # The message must be hashed before signing with KMS
    # For simplicity, we'll assume the payload["message"] is already hashed or a short message
    # In a real scenario, you'd hash the message using a crypto library like hashlib

    response = kms_client.sign(
        KeyId=config["key_id"],
        Message=payload["message"],
        MessageType="RAW",  # or "DIGEST" if already hashed
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA256", # or other supported algorithms
    )
    return {"signature": base64.b64encode(response["Signature"]).decode("utf-8")}


def verify_signature(payload, config=None):
    config = config or {}
    kms_client = boto3.client("kms", region_name=config.get("region"))

    response = kms_client.verify(
        KeyId=config["key_id"],
        Message=payload["message"],
        MessageType="RAW",  # or "DIGEST"
        Signature=base64.b64decode(payload["signature"]),
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA256", # must match signing algorithm
    )
    return {"signature_valid": response["SignatureValid"]}
