import boto3

from security_models import decode_blob, normalize_payload


def decrypt_payload(payload, config=None):
    payload = normalize_payload(payload)
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    response = client.decrypt(CiphertextBlob=decode_blob(payload["ciphertext"]))
    return {"plaintext": response["Plaintext"]}
