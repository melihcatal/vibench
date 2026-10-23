import os

def get_perspective_api_key():
    return os.getenv('PERSPECTIVE_API_KEY')

def get_tisane_api_key():
    return os.getenv('TISANE_API_KEY')

def get_azure_content_safety_endpoint():
    return os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')

def get_azure_content_safety_key():
    return os.getenv('AZURE_CONTENT_SAFETY_KEY')

def get_aws_access_key_id():
    return os.getenv('AWS_ACCESS_KEY_ID')

def get_aws_secret_access_key():
    return os.getenv('AWS_SECRET_ACCESS_KEY')