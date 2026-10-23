import boto3

def sign_or_verify_key(key_id, message, signature=None):
    kms_client = boto3.client('kms')
    if signature is not None:
        try:
            kms_client.verify(
                KeyId=key_id,
                Message=message,
                Signature=signature
            )
            return 'Verification successful'
        except boto3.exceptions.botocore.client.ClientError as e:
            return f'Verification failed: {e}'
    else:
        response = kms_client.sign(
            KeyId=key_id,
            Message=message
        )
        return response['Signature']

# Example usage:
# signature = sign_or_verify_key('alias/myKey', b'message to sign')
# result = sign_or_verify_key('alias/myKey', b'message to verify', signature)