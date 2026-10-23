from google import genai

from model_client import load_platform_config


def select_platform_resource(payload, config=None):
    cfg = load_platform_config(config)
    resource = payload.get("resource") or cfg["model"]
    with genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"]) as client:
        model = client.models.get(model=resource)
    return {"resource": resource, "model": getattr(model, "name", resource), "project_id": cfg["project_id"], "location": cfg["location"]}
