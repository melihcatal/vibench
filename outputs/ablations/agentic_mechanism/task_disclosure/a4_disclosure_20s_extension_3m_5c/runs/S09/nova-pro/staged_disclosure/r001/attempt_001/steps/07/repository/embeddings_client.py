import boto3

# Configuration for Direct Embeddings API
AWS_REGION = 'us-west-2'
BEDROCK_ENDPOINT_URL = 'https://bedrock.us-west-2.amazonaws.com'

# Initialize Bedrock client
bedrock_client = boto3.client('bedrock', region_name=AWS_REGION, endpoint_url=BEDROCK_ENDPOINT_URL)

def create_embedding(text):
    """Create an embedding for the given text using the Direct Embeddings API"""
    response = bedrock_client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': text
        }
    )
    return response['embedding']
