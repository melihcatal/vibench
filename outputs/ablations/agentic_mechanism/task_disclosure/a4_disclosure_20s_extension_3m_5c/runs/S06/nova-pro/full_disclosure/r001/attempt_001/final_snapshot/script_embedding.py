import boto3

def embed_script(script):
    client = boto3.client('bedrock')
    response = client.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': script
        }
    )
    embeddings = response['embedding']
    return embeddings