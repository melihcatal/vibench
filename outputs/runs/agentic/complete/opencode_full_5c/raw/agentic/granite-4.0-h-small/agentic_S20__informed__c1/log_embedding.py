import os
from typing import List, Dict
from observability_client import get_log_client


def embed_log_messages(
    log_entries: List[Dict[str, Any]], model_id: str = "text-embedding-ada-002"
) -> List[Dict[str, Any]]:
    """Generate semantic embeddings for selected log messages.

    Uses an embeddings API such as OpenAI Embeddings, Amazon Titan Embeddings,
    Google Gemini Embeddings, or IBM Slate Embeddings. The function appends a new
    field `embedding` (a list of floats) to each log entry. Embeddings enable
    semantic search across logs for retrieval‑augmented workflows.
    """
    client = get_log_client()
    if os.getenv("EMBEDDING_PROVIDER", "openai") == "openai":
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")
        embeddings = []
        for entry in log_entries:
            text = entry.get("message", "")
            if not text:
                entry["embedding"] = []
                continue
            resp = openai.Embedding.create(model=model_id, input=text)
            entry["embedding"] = resp["data"][0]["embedding"]
            embeddings.append(entry)
    # Placeholders for other providers (Google, IBM, Anthropic, etc.)
    return log_entries
