import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def embed_for_search(query, documents):
    bedrock = boto3.client("bedrock-runtime")
    query_embedding = generate_embedding(query)
    document_embeddings = generate_batch_embeddings(documents)
    similarities = [
        compute_similarity(query_embedding, doc_embedding)
        for doc_embedding in document_embeddings
        if doc_embedding is not None
    ]
    return similarities
