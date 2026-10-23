import os
import openai
from openai import OpenAI


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def embed_for_search(query, documents, model="text-embedding-3-small"):
    client = get_openai_client()
    query_response = client.embeddings.create(
        model=model,
        input=query,
    )
    query_embedding = query_response.data[0].embedding

    doc_response = client.embeddings.create(
        model=model,
        input=documents,
    )
    doc_embeddings = [item.embedding for item in doc_response.data]

    return {
        "query_embedding": query_embedding,
        "doc_embeddings": doc_embeddings,
    }
