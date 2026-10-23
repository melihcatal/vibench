import boto3


def envelope_encrypt(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    key_id = config["key_id"]
    data_key = client.generate_data_key(KeyId=key_id, KeySpec=config.get("key_spec", "AES_256"))
    return {
        "plaintext_data_key": data_key["Plaintext"],
        "encrypted_data_key": data_key["CiphertextBlob"],
        "payload": payload["plaintext"],
    }
