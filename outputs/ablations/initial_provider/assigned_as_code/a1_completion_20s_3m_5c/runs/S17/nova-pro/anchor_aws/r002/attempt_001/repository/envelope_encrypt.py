import boto3


def envelope_encrypt(data, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    response = client.generate_data_key(KeyId=config["key_id"], KeySpec='AES_256')
    ciphertext_blob = response['CiphertextBlob']
    plaintext_key = response['Plaintext']
    encrypted_data = boto3.client('kms').encrypt(KeyId=config["key_id"], Plaintext=data['plaintext'])['CiphertextBlob']
    return {'ciphertext': ciphertext_blob, 'encrypted_data': encrypted_data}