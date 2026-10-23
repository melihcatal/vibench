import boto3


def decrypt_payload(ciphertext):
    kms_client = boto3.client("kms", region_name="us-west-2")
    response = kms_client.decrypt(CiphertextBlob=ciphertext)
    return response["Plaintext"]
