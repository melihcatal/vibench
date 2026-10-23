import os
import boto3
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def get_azure_document_intelligence_client(config: dict):
    endpoint = config.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT') or os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    api_key = config.get('AZURE_DOCUMENT_INTELLIGENCE_API_KEY') or os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_API_KEY')
    if not endpoint or not api_key:
        raise ValueError("Azure Document Intelligence endpoint and API key must be provided.")
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key))

def get_aws_textract_client(config: dict):
    aws_access_key_id = config.get('AWS_ACCESS_KEY_ID') or os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = config.get('AWS_SECRET_ACCESS_KEY') or os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region_name = config.get('AWS_REGION_NAME') or os.environ.get('AWS_REGION_NAME') or 'us-east-1'

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS access key ID and secret access key must be provided.")

    return boto3.client(
        'textract',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region_name
    )
