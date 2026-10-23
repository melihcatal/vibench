from google import genai

from model_client import load_platform_config


def platform_output_embedding(payload, config=None):
    cfg = load_platform_config(config)
    with genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"]) as client:
        response = client.models.embed_content(model="text-embedding-004", contents=payload["text"])
    embedding = getattr(response, "embeddings", None)
    return {"embedding": embedding, "model": "text-embedding-004"}
