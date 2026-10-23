from google import genai

from model_client import load_platform_config


def collect_platform_metadata(payload, config=None):
    cfg = load_platform_config(config)
    with genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"]) as client:
        response = client.models.generate_content(model=cfg["model"], contents=payload["text"])
    return {
        "text": response.text or "",
        "usage": getattr(response, "usage_metadata", None),
        "model": getattr(response, "model_version", cfg["model"]),
        "resource_id": getattr(response, "name", None),
    }
