import boto3

def create_embeddings_client():
    client = boto3.client('sagemaker-runtime', region_name='us-west-2')
    return client