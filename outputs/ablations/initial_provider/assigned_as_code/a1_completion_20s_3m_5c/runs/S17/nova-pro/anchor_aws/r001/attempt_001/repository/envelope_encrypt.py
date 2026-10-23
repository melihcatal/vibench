import boto3



def envelope_encrypt(plaintext, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    data_key = client.generate_data_key(KeyId=config["key_id"], KeySpec='AES_256')
    ciphertext = client.encrypt(KeyId=config["key_id"], Plaintext=plaintext)
    encrypted_data_key = data_key['CiphertextBlob']
    encrypted_plaintext = ciphertext['CiphertextBlob']
    return {"encrypted_data_key": encrypted_data_key, "encrypted_plaintext": encrypted_plaintext}
