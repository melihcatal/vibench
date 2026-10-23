import boto3

def generate_embeddings(texts):
    client = boto3.client('bedrock')
    response = client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': texts
        }
    )
    return response['embeddings']