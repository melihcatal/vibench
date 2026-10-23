import boto3

def embed_query(query):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': query}
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding

def embed_documents(documents):
    embeddings = []
    for doc in documents:
        embedding = embed_query(doc)
        embeddings.append(embedding)
    return embeddings