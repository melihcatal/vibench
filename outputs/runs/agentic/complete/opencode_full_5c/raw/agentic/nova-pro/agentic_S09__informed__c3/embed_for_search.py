import boto3


def embed_for_search(query, documents):
    client = boto3.client("bedrock-runtime")
    query_embedding = generate_embedding(query)
    document_embeddings = generate_batch_embeddings(documents)
    similarities = [
        compute_similarity(query_embedding, doc_emb) for doc_emb in document_embeddings
    ]
    return similarities
