import os
import openai
from typing import List, Dict
from observability_models import NormalizedLogRecord

# OpenAI Embeddings API is used as the concrete external provider.
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")


def log_embedding(logs: List[NormalizedLogRecord]) -> List[Dict[str, str]]:
    """Create embeddings for a list of NormalizedLogRecord dictionaries.
    Returns a list of dicts each containing the original log ID (index) and the embedding vector.
    """
    messages = [log["message"] for log in logs]
    response = openai.Embedding.create(model=MODEL, input=messages)
    embeddings = []
    for i, vec in enumerate(response["data"]):
        embeddings.append({
            "log_index": str(i),
            "embedding": " ".join(map(str, vec["embedding"]))
        })
    return embeddings
