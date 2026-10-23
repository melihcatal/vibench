import os

from google import genai


def output_embedding(payload, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["GOOGLE_API_KEY"]
    model = config.get("model") or "text-embedding-004"
    with genai.Client(api_key=api_key) as client:
        response = client.models.embed_content(model=model, contents=payload["text"])
    return {"embedding": response.embeddings[0].values if getattr(response, "embeddings", None) else []}
