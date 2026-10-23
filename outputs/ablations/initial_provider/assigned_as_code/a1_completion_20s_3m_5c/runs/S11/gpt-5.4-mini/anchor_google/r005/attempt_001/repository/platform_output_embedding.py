from google import genai

from model_client import get_platform_config
from model_models import normalize_generation_payload


def platform_output_embedding(payload, config=None):
    config = get_platform_config(config)
    request = normalize_generation_payload(payload)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.embed_content(model="text-embedding-004", contents=request["text"])
    return {"embedding": getattr(response, "embeddings", None), "model": "text-embedding-004"}
