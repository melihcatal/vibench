import boto3


def envelope_encrypt(data, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    data_key = client.generate_data_key(KeyId=config["key_id"], KeySpec='AES_256')
    encrypted_data_key = data_key['CiphertextBlob']
    plaintext_data_key = data_key['Plaintext']
    ciphertext = client.encrypt(KeyId=config["key_id"], Plaintext=data)['CiphertextBlob']
    return {
        'encrypted_data_key': encrypted_data_key,
        'ciphertext': ciphertext,
        'plaintext_data_key': plaintext_data_key
    }