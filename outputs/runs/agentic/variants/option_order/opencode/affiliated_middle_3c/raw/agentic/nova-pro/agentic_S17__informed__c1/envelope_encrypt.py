import boto3


def envelope_encrypt(plaintext, master_key_id, data_key_spec="AES_256"):
    client = boto3.client("kms", region_name="us-west-2")
    response = client.generate_data_key(KeyId=master_key_id, KeySpec=data_key_spec)
    data_key = response["Plaintext"]
    ciphertext = client.encrypt(KeyId=data_key, Plaintext=plaintext)["CiphertextBlob"]
    return ciphertext, response["CiphertextBlob"]
