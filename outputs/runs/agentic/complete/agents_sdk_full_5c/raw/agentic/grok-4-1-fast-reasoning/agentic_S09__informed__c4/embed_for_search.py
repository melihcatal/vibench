import os
from openai import OpenAI
from embeddings_client import EMBEDDING_MODEL
from embeddings_models import search_similarities
from typing import List

def embed_single(text: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def embed_documents(texts: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL
    )
    return [data.embedding for data in response.data]

def embed_for_search(query: str, documents: List[str]) -> List[float]:
    query_emb = embed_single(query)
    doc_embs = embed_documents(documents)
    return search_similarities(query_emb, doc_embs)