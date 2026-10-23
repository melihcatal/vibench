import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def embed_text(text):
    model_id = 'amazon.titan-embed-text-v1'
    body = {
        'inputText': text
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding

if __name__ == '__main__':
    query = 'example query'
    documents = ['example document 1', 'example document 2']
    query_embedding = embed_text(query)
    document_embeddings = [embed_text(doc) for doc in documents]
    print('Query Embedding:', query_embedding)
    print('Document Embeddings:', document_embeddings)