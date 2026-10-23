import os
from dashscope import TextEmbedding


def embed_for_search(query: str, documents: list) -> list:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    query_embedding = TextEmbedding.call(
        model="text-embedding-v1", input=query, api_key=api_key
    )["output"]["embeddings"][0]["vector"]
    document_embeddings = TextEmbedding.call(
        model="text-embedding-v1", input=documents, api_key=api_key
    )["output"]["embeddings"]
    scores = [
        dot(query_embedding, doc["vector"])
        / (norm(query_embedding) * norm(doc["vector"]))
        for doc in document_embeddings
    ]
    return sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
