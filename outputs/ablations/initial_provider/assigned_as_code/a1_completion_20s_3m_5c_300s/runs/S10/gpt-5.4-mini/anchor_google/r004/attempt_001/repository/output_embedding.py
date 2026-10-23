import os

from google import genai

from model_client import build_model_config, get_api_key


def output_embedding(payload, config=None):
    config = build_model_config(config)
    text = payload.get("text", "")
    with genai.Client(api_key=get_api_key(config, "GOOGLE_API_KEY")) as client:
        response = client.models.embed_content(model=config.get("embedding_model") or "text-embedding-004", contents=text)
    embedding = getattr(response, "embeddings", None)
    if embedding:
        return {"embedding": embedding[0].values}
    values = getattr(response, "values", None) or []
    return {"embedding": values}
