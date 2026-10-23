import os

from google import genai


def get_client(config=None):
    config = config or {}
    return genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"])