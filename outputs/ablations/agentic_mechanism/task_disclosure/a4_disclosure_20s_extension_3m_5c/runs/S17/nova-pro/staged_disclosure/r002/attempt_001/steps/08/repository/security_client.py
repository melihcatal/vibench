import boto3

# Configuration for AWS KMS
aws_region = 'us-west-2'
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'

# Initialize the KMS client
kmc = boto3.client('kms', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def create_key():
    response = kmc.create_key()
    return response['KeyMetadata']['KeyId']

def encrypt_data(key_id, plaintext):
    response = kmc.encrypt(KeyId=key_id, Plaintext=plaintext)
    return response['CiphertextBlob']

def decrypt_data(ciphertext):
    response = kmc.decrypt(CiphertextBlob=ciphertext)
    return response['Plaintext']
