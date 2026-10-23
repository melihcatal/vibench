import boto3

def embed_for_search(query, documents):
    bedrock_client = boto3.client('bedrock-runtime')
    embeddings = []
    for text in [query] + documents:
        response = bedrock_client.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': text
            }
        )
        embedding = response['embedding']
        embeddings.append(embedding)
    return embeddings