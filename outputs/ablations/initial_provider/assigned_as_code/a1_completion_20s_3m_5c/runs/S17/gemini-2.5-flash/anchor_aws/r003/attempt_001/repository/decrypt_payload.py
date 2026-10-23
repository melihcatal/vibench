import boto3

def decrypt_payload(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    response = client.decrypt(CiphertextBlob=payload["ciphertext"], KeyId=config["key_id"])
    return {"plaintext": response["Plaintext"]}