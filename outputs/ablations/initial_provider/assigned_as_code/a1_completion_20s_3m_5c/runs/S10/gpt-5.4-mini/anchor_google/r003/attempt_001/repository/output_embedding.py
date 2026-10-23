from google import genai

from model_client import get_api_key


def output_embedding(payload, config=None):
    config = config or {}
    with genai.Client(api_key=get_api_key(config)) as client:
        response = client.models.embed_content(model="text-embedding-004", contents=payload["text"])
    return {"embedding": getattr(response, "embedding", None)}
