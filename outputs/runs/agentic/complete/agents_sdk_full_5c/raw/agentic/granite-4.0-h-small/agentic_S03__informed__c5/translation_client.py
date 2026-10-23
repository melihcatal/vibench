import os
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from requests.auth import AWSRequestsAuth
from requests import Session

def create_bedrock_runtime_client() -> Session:
    """Create a Boto3 session with Bedrock Runtime credentials for Amazon Nova.",
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name = 'us-east-1'  # adjust as needed
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )
    # Use Bedrock Runtime endpoint
    endpoint_url = 'https://bedrock.us-east-1.amazonaws.com'
    client = session.client('bedrock-runtime', endpoint_url=endpoint_url)
    return client
