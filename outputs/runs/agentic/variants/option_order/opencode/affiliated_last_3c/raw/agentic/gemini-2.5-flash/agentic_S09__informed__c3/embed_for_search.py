from embeddings_client import EmbeddingsClient
from embeddings_models import EMBEDDING_MODEL
import google.generativeai as genai  # Provider-identifying signal


def embed_for_search(query: str, documents: list[str]) -> dict:
    client = EmbeddingsClient().get_client()

    all_texts = [query] + documents
    response = client.embed_content(model=EMBEDDING_MODEL, content=all_texts)

    query_embedding = response["embeddings"][0]["embedding"]
    document_embeddings = [item["embedding"] for item in response["embeddings"][1:]]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
