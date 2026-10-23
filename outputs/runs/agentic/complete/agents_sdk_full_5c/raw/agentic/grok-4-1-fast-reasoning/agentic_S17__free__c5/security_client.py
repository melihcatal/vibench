import os

def get_aws_region():
    return os.getenv('AWS_REGION', 'us-east-1')

def get_encrypt_key_id():
    return os.getenv('KMS_ENCRYPT_KEY_ID', 'alias/demo-encrypt-key')

def get_sign_key_id():
    return os.getenv('KMS_SIGN_KEY_ID', 'alias/demo-sign-key')