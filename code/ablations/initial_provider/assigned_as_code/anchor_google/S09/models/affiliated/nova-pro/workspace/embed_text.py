import os

from google import genai


def embed_text(payload, config=None):
    config = config or {}
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        response = client.models.embed_content(model="gemini-embedding-001", contents=payload["text"])
    return {"embedding": list(response.embeddings[0].values)}
