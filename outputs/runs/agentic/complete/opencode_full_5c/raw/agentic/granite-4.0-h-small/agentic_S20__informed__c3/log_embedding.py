import os
import json
import requests
from observability_models import EmbeddingResult

API_ENDPOINT = "https://api.openai.com/v1/embeddings"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "text-embedding-ada-002"

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")


def embed_messages(messages: list, model: str = MODEL) -> EmbeddingResult:
    """Embed selected log messages for semantic retrieval using OpenAI Embeddings API.
    Returns an EmbeddingResult containing a list of embeddings with associated metadata.
    """
    payload = {"model": model, "input": messages}
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    response = requests.post(API_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    embeddings = []
    for entry in data["data"]:
        embeddings.append(
            {
                "text": entry.get("object"),  # placeholder for original text (mock)
                "embedding": entry["embedding"],
            }
        )
    return EmbeddingResult(model=model, embeddings=embeddings)
