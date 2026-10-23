import google.generativeai as genai
from observability_client import ObservabilityClient


def embed_log_message(message: str) -> list[float]:
    client = ObservabilityClient()

    result = genai.embed_content(
        model=client.gemini_embedding_model,
        content=message,
        task_type="RETRIEVAL_QUERY",
    )
    return result["embedding"]
