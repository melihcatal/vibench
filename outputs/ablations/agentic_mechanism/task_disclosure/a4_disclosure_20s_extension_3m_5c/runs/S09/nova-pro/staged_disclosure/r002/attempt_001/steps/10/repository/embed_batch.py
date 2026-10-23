import boto3

def generate_embeddings(texts):
    bedrock = boto3.client('bedrock')
    response = bedrock.embeddings(texts=texts)
    return response['embeddings']