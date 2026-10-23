import boto3

kms = boto3.client("kms", region_name="us-west-2")


def decrypt_payload(ciphertext):
    response = kms.decrypt(CiphertextBlob=ciphertext)
    return response["Plaintext"]
