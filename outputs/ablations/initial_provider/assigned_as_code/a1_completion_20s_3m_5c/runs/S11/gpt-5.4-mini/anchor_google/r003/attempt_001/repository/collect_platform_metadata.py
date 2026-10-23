from google import genai

from model_models import normalize_platform_metadata
from model_client import load_platform_config


def collect_platform_metadata(payload, config=None):
    config = load_platform_config(config)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=payload.get("model") or config["model"], contents=payload["text"])
    return normalize_platform_metadata(response)
