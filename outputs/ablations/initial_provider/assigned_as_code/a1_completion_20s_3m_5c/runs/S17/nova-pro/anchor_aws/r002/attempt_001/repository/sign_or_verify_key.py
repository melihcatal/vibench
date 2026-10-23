import boto3


def sign_or_verify_key(message, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    response = client.sign(KeyId=config["key_id"], Message=message["message"], MessageType='RAW')
    return {'signature': response['Signature']}