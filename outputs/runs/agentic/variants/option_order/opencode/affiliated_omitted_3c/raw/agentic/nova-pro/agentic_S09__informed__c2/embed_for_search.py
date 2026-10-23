import os
from dashscope import TextEmbedding


def embed_for_search(query: str, documents: list) -> tuple:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    query_embedding = TextEmbedding.call(
        model="text-embedding-v1", input=query
    ).output.embedding
    document_embeddings = [
        TextEmbedding.call(model="text-embedding-v1", input=doc).output.embedding
        for doc in documents
    ]
    return query_embedding, document_embeddings
