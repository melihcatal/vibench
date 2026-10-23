from google import genai


def load_platform_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id"),
        "location": config.get("location", "us-central1"),
        "model": config.get("model", "gemini-2.5-flash"),
        "locale": config.get("locale", "en"),
    }


def build_vertex_client(config=None):
    cfg = load_platform_config(config)
    return genai.Client(vertexai=True, project=cfg["project_id"], location=cfg["location"]), cfg
