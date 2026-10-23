import boto3


def decrypt_payload(ciphertext, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    response = client.decrypt(CiphertextBlob=ciphertext["ciphertext"])
    return {"plaintext": response["Plaintext"].decode()}