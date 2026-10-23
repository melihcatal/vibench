from google import genai

from model_client import load_platform_config


def platform_output_embedding(payload, config=None):
    config = load_platform_config(config)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.embed_content(model="text-embedding-004", contents=payload["text"])
    return {"embedding": getattr(response, "embeddings", None) or getattr(response, "embedding", None)}
