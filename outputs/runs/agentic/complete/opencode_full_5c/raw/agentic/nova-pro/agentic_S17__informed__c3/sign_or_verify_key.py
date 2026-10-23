import boto3


def sign_or_verify_key(operation, message):
    kms_client = boto3.client("kms", region_name="us-west-2")
    if operation == "sign":
        response = kms_client.sign(
            KeyId="alias/example_key", Message=message, MessageType="RAW"
        )
        return response["Signature"]
    elif operation == "verify":
        response = kms_client.verify(
            KeyId="alias/example_key",
            Message=message,
            MessageType="RAW",
            Signature=message,
        )
        return response["SignatureValid"]
