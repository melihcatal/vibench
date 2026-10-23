import boto3

def encrypt_payload(plaintext):
    client = boto3.client('kms', region_name='us-west-2')
    key_id = 'arn:aws:kms:us-west-2:123456789012:key/abcdefgh-1234-5678-9012-abcdefghijkl'
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response['CiphertextBlob']