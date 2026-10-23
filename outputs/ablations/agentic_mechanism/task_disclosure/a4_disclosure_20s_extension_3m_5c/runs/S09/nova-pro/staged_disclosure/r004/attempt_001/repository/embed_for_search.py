import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def embed_query(query):
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': query
        }
    )
    result = json.loads(response['body'].read())
    return result['embedding']

def embed_documents(documents):
    embeddings = []
    for doc in documents:
        response = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': doc
            }
        )
        result = json.loads(response['body'].read())
        embeddings.append(result['embedding'])
    return embeddings