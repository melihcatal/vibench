import boto3

def generate_embeddings(texts):
    client = boto3.client('bedrock')
    response = client.generate_embeddings(Texts=texts)
    return response['Embeddings']