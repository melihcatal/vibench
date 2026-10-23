import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.config import Config
import boto3

BEDROCK_REGION = 'us-east-1'
EMBEDDINGS_MODEL_ID = 'amazon.titan-embed-text-v1'

def create_bedrock_client():
    config = Config(
        region_name=BEDROCK_REGION,
        retries={'max_attempts': 10},
    )
    try:
        client = boto3.client('bedrock-runtime', config=config)
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise ValueError('AWS credentials not found or incomplete')
    return client

def embeddings_request(client, text):
    response = client.invoke_model(
        model_id=EMBEDDINGS_MODEL_ID,
        body={
            'inputText': text,
        }
    )
    return response

if __name__ == '__main__':
    client = create_bedrock_client()
    sample_text = 'This is a sample text for embedding.'
    response = embeddings_request(client, sample_text)
    print(response)