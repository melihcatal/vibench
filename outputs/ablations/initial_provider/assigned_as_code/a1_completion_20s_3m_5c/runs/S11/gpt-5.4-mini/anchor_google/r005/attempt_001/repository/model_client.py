import os


def get_platform_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        "location": config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        "model": config.get("model") or os.environ.get("VERTEXAI_MODEL", "gemini-2.5-flash"),
    }
