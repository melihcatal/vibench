import os

from google import genai


def embed_batch(payload, config=None):
    config = config or {}
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        response = client.models.embed_content(model="gemini-embedding-001", contents=payload["texts"])
    return {"embeddings": [list(embedding.values) for embedding in response.embeddings]}
