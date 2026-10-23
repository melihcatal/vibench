import os

from google import genai


def embed_for_search(payload, config=None):
    config = config or {}
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        query_embedding_response = client.models.embed_content(model="gemini-embedding-001", contents=payload["query"], task_type="SEMANTIC_SIMILARITY", title="query")
        document_embeddings_response = client.models.embed_content(model="gemini-embedding-001", contents=payload["documents"], task_type="SEMANTIC_SIMILARITY", title="document")
    
    return {
        "query_embedding": list(query_embedding_response.embeddings[0].values),
        "document_embeddings": [list(embedding.values) for embedding in document_embeddings_response.embeddings]
    }
