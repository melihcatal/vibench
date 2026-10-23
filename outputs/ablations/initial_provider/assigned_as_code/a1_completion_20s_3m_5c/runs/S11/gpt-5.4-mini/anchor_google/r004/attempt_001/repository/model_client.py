import os
from google import genai


def load_platform_config(overrides=None):
    overrides = overrides or {}
    return {
        "project_id": overrides.get("project_id") or os.getenv("GOOGLE_CLOUD_PROJECT"),
        "location": overrides.get("location") or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        "model": overrides.get("model") or os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-flash"),
    }


def create_platform_client(config=None):
    config = config or load_platform_config()
    return genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
