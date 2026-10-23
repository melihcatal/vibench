import boto3

def embed_query_and_documents(query, documents):
    bedrock_client = boto3.client('bedrock', region_name='us-west-2')
    embeddings = []
    for text in [query] + documents:
        response = bedrock_client.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': text
            }
        )
        embeddings.append(response['embedding'])
    return embeddings