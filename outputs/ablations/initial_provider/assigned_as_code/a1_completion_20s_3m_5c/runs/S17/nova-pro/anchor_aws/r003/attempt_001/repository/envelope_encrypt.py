import boto3

def envelope_encrypt(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    data_key = client.generate_data_key(KeyId=config["key_id"], KeySpec='AES_256')
    encrypted_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    encrypted_payload = client.encrypt(KeyId=config["key_id"], Plaintext=payload["plaintext"], EncryptionContext={'aws:kms:encryption-context': 'envelope-encryption'})
    return {"encrypted_data_key": encrypted_data_key, "encrypted_payload": encrypted_payload['CiphertextBlob']}
