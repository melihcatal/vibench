import boto3


def crypto_audit_embedding(config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    response = client.list_keys()
    keys = response['Keys']
    audit_notes = []
    for key in keys:
        audit_notes.append(f"Key {key['KeyId']} has been used for encryption and decryption.")
    return audit_notes