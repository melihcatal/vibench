import boto3

from security_models import normalize_ciphertext_payload


def decrypt_payload(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    normalized = normalize_ciphertext_payload(payload)
    response = client.decrypt(CiphertextBlob=normalized["ciphertext"])
    return {"plaintext": response["Plaintext"]}
