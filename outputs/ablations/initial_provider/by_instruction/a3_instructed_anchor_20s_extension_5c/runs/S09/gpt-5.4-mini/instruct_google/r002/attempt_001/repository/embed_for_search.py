from embeddings_client import configure_client, embedding_model, task_type
from embeddings_models import normalize_vector
import google.generativeai as genai


def embed_for_search(query: str, documents: list[str]) -> dict[str, object]:
    configure_client()
    query_result = genai.embed_content(model=embedding_model(), content=query, task_type="retrieval_query")
    document_result = genai.embed_content(model=embedding_model(), content=documents, task_type=task_type())
    return {
        "query_embedding": normalize_vector([float(v) for v in query_result["embedding"]]),
        "document_embeddings": [normalize_vector([float(v) for v in item["embedding"]]) for item in document_result["embedding"]],
    }
