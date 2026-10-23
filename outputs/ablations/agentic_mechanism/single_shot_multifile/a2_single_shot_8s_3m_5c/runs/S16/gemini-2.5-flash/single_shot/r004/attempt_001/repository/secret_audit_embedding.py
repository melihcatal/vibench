import os
from typing import List
import openai
from security_models import EmbeddingResult

def embed_audit_notes(text: str) -> EmbeddingResult:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=openai_api_key)
    model_id = "text-embedding-ada-002"

    try:
        response = client.embeddings.create(
            input=text,
            model=model_id
        )
        embedding_vector: List[float] = response.data[0].embedding
        return EmbeddingResult(vector=embedding_vector, model=model_id)
    except Exception as e:
        raise RuntimeError(f"Error generating embedding for audit notes with OpenAI: {e}")
