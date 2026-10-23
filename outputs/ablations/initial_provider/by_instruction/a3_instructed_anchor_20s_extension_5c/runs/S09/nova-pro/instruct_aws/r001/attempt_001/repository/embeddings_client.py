import boto3

def get_embeddings_client():
    return boto3.client('sagemaker-runtime')