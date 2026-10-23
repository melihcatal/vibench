import os

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
TISANE_API_KEY = os.getenv('TISANE_API_KEY')
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def get_perspective_api_key():
    return PERSPECTIVE_API_KEY

def get_tisane_api_key():
    return TISANE_API_KEY

def get_azure_content_safety_client():
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    return ContentSafetyClient(AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY))

def get_aws_comprehend_client():
    import boto3
    return boto3.client('comprehend', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')