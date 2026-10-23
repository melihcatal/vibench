import boto3

def generate_embeddings(texts):
    client = boto3.client('bedrock-runtime')
    embeddings = []
    for text in texts:
        response = client.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': text
            }
        )
        embedding = response['embedding']
        embeddings.append(embedding)
    return embeddings