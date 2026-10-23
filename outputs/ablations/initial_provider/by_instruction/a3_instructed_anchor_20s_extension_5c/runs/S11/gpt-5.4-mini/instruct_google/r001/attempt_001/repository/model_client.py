import os
from functools import lru_cache

from google import genai


@lru_cache(maxsize=1)
def get_client():
    api_key = os.environ.get("GOOGLE_API_KEY")
    return genai.Client(api_key=api_key)


def get_model_name(default="gemini-2.5-flash"):
    return os.environ.get("GOOGLE_GENAI_MODEL", default)


def get_configured_region(default="global"):
    return os.environ.get("GOOGLE_CLOUD_REGION", default)
