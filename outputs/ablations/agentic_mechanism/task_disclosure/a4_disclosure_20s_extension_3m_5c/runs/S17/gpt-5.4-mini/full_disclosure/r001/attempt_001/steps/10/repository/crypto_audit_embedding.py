import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def embed_crypto_audit_notes(notes: List[str], model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    embedding_model = model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    response = client.embeddings.create(model=embedding_model, input=notes)
    return {
        "provider": "openai",
        "model": embedding_model,
        "vectors": [item.embedding for item in response.data],
    }
