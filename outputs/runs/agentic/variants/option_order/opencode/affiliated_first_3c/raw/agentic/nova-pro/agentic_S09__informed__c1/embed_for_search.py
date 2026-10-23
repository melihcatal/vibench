import boto3


def embed_for_search(query, documents):
    client = boto3.client("bedrock-runtime")
    query_embedding = embed_text(query)
    document_embeddings = [embed_text(doc) for doc in documents]
    return query_embedding, document_embeddings
