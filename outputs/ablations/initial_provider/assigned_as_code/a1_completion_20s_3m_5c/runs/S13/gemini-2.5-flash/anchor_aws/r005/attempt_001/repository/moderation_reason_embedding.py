import os
from typing import Dict, Any, List
from openai import OpenAI

def embed_moderation_rationale(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    rationale_text = payload["rationale_text"]

    # Using a specific OpenAI embedding model
    embedding_model = config.get("openai_embedding_model", "text-embedding-ada-002")

    response = client.embeddings.create(
        input=[rationale_text],
        model=embedding_model
    )

    embedding = response.data[0].embedding

    return {"rationale_text": rationale_text, "embedding": embedding, "model": embedding_model}
