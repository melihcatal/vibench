import os
from openai import OpenAI
from typing import List, Dict
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingVector

def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[EmbeddingVector]]:
    client = get_openai_client()
    all_texts = [query] + documents
    response = client.embeddings.create(
        input=all_texts,
        model="text-embedding-ada-002"
    )
    query_embedding = response.data[0].embedding
    document_embeddings = [item.embedding for item in response.data[1:]]
    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings
    }