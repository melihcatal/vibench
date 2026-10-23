import boto3


def embed_for_search(query, documents):
    client = boto3.client("bedrock-runtime")
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)
    scores = [
        similarity_score(query_embedding, doc_embedding)
        for doc_embedding in document_embeddings
    ]
    return scores
