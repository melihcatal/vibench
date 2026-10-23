import boto3


def encrypt_payload(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    response = client.encrypt(KeyId=config["key_id"], Plaintext=payload["plaintext"])
    return {"ciphertext": response["CiphertextBlob"]}
