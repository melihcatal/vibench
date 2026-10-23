import boto3

def embed_for_search(query, documents):
    bedrock = boto3.client('bedrock-runtime')

    query_embedding = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': query
        }
    )

    document_embeddings = []
    for doc in documents:
        document_embedding = bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': doc
            }
        )
        document_embeddings.append(document_embedding)

    return query_embedding, document_embeddings