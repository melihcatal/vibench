from google import genai

from model_client import get_platform_config
from model_models import normalize_resource_selection


def select_platform_resource(payload, config=None):
    config = get_platform_config(config)
    selection = normalize_resource_selection(payload)
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        model = selection.get("model") or config["model"]
        return {"resource": model, "project_id": config["project_id"], "location": config["location"]}
