import boto3

def embed_for_search(query, documents):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'

    query_embedding = bedrock.invoke_model(
        modelId=model_id,
        body={
            'inputText': query
        }
    )
    document_embeddings = []
    for doc in documents:
        doc_embedding = bedrock.invoke_model(
            modelId=model_id,
            body={
                'inputText': doc
            }
        )
        document_embeddings.append(doc_embedding)
    return query_embedding, document_embeddings