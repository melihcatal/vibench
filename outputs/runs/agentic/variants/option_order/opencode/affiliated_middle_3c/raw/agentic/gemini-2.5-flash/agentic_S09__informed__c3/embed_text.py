import google.generativeai as genai
from embeddings_client import configure_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_text(text: str) -> list[float]:
    configure_embeddings_client()
    response = genai.embed_content(
        model="embedding-001", content=text, task_type="SEMANTIC_SIMILARITY"
    )
    return normalize_embedding_response(response)
