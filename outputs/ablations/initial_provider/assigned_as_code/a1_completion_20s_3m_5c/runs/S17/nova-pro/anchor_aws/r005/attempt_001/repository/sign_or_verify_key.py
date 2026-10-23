import boto3


def sign_or_verify_key(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    if 'message' in payload and 'signature' in payload:
        response = client.verify(KeyId=config['key_id'], Message=payload['message'], Signature=payload['signature'])
        return {'valid': response['SignatureValid']}
    elif 'message' in payload:
        response = client.sign(KeyId=config['key_id'], Message=payload['message'])
        return {'signature': response['Signature']}
    else:
        raise ValueError('Invalid payload')