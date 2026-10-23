import boto3

def get_s3_client():
    """
    Provides a configured boto3 S3 client.
    """
    # AWS region can be configured via environment variables (AWS_REGION, AWS_DEFAULT_REGION)
    # or ~/.aws/config, or passed directly to client (e.g., region_name='us-east-1')
    # For this example, we rely on standard boto3 credential chain.
    return boto3.client('s3')

def get_textract_client():
    """
    Provides a configured boto3 Textract client.
    """
    return boto3.client('textract')

def get_translate_client():
    """
    Provides a configured boto3 Translate client.
    """
    return boto3.client('translate')

def get_bedrock_runtime_client():
    """
    Provides a configured boto3 Bedrock Runtime client.
    """
    # Bedrock models are region-specific, ensure your region supports Bedrock
    return boto3.client('bedrock-runtime')

