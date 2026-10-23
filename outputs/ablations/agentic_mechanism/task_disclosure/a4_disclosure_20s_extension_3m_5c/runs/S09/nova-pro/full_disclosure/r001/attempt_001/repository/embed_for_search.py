import boto3

bedrock = boto3.client('bedrock-runtime')

MODEL_ID = 'amazon.titan-embed-text-v1'

def embed_text(text):
    body = {
        'inputText': text
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=MODEL_ID,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding

def embed_for_search(query, documents):
    query_embedding = embed_text(query)
    document_embeddings = [embed_text(doc) for doc in documents]
    return query_embedding, document_embeddings