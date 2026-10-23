import boto3


def sign_or_verify_key(payload, action, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    if action == 'sign':
        response = client.sign(KeyId=config["key_id"], Message=payload["message"], MessageType='RAW')
        return {"signature": response["Signature"]}
    elif action == 'verify':
        response = client.verify(KeyId=config["key_id"], Message=payload["message"], Signature=payload["signature"], MessageType='RAW')
        return {"verified": response["SignatureValid"]}
    else:
        raise ValueError("Invalid action. Use 'sign' or 'verify'.")