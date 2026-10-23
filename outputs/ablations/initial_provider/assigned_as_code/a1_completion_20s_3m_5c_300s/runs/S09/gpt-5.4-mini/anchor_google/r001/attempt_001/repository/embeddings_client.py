import os

from google import genai


def load_config(config=None):
    config = config or {}
    return {"api_key": config.get("api_key") or os.environ["GOOGLE_API_KEY"], "model": config.get("model") or "gemini-embedding-001"}


def client_for(config=None):
    cfg = load_config(config)
    return genai.Client(api_key=cfg["api_key"]), cfg
