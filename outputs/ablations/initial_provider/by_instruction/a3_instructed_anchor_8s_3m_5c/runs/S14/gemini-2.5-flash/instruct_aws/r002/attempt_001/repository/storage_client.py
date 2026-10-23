import boto3
from botocore.config import Config

def get_s3_client():
    # AWS S3 client with a specific configuration
    s3_config = Config(
        region_name='us-east-1',
        signature_version='s3v4',
    )
    return boto3.client('s3', config=s3_config)

def get_textract_client():
    # AWS Textract client
    return boto3.client('textract', region_name='us-east-1')

def get_translate_client():
    # AWS Translate client
    return boto3.client('translate', region_name='us-east-1')

def get_comprehend_client():
    # AWS Comprehend client for summarization and entity extraction
    return boto3.client('comprehend', region_name='us-east-1')

def get_bedrock_runtime_client():
    # AWS Bedrock Runtime client for embedding models like Titan Embedding
    return boto3.client('bedrock-runtime', region_name='us-east-1')
