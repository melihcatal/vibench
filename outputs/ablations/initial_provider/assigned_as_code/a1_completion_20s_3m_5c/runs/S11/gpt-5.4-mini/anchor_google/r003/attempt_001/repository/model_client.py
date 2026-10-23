from google import genai
from google.genai import types


def load_platform_config(config=None):
    config = config or {}
    return {
        "project_id": config.get("project_id"),
        "location": config.get("location", "us-central1"),
        "model": config.get("model", "gemini-2.5-flash"),
        "temperature": config.get("temperature", 0.2),
        "max_output_tokens": config.get("max_output_tokens"),
    }


def make_vertex_client(config):
    return genai.Client(vertexai=True, project=config["project_id"], location=config["location"])


def text_contents(payload):
    if isinstance(payload, dict):
        if "text" in payload:
            return payload["text"]
        if "contents" in payload:
            return payload["contents"]
    return payload


def to_generate_config(config):
    kwargs = {"temperature": config.get("temperature", 0.2)}
    if config.get("max_output_tokens") is not None:
        kwargs["max_output_tokens"] = config["max_output_tokens"]
    return types.GenerateContentConfig(**kwargs)
