import os
from google import genai


def load_platform_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ["GOOGLE_CLOUD_PROJECT"],
        "location": config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        "model": config.get("model", "gemini-2.5-flash"),
    }


def get_platform_client(config=None):
    cfg = load_platform_config(config)
    return genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"])
