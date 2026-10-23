import boto3


def sign_or_verify_key(operation, key_id, message):
    kms_client = boto3.client("kms")
    if operation == "sign":
        response = kms_client.sign(KeyId=key_id, Message=message)
        return response["Signature"]
    elif operation == "verify":
        response = kms_client.verify(KeyId=key_id, Message=message, Signature=message)
        return response["SignatureValid"]
