import boto3


def decrypt_payload(ciphertext, key_id):
    client = boto3.client("kms", region_name="us-west-2")
    response = client.decrypt(KeyId=key_id, CiphertextBlob=ciphertext)
    return response["Plaintext"]
