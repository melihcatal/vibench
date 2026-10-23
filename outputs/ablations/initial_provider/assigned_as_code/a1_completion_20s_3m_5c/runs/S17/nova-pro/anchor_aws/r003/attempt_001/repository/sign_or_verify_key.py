import boto3

def sign_or_verify_key(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    if config.get("sign"):
        response = client.sign(KeyId=config["key_id"], Message=payload["plaintext"], MessageType='RAW')
        return {"signature": response['Signature']}
    else:
        response = client.verify(KeyId=config["key_id"], Message=payload["plaintext"], Signature=payload["signature"], MessageType='RAW')
        return {"verified": response['SignatureValid']}
