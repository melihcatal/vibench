import os
from google import genai


DEFAULT_MODEL_ID = "gemini-2.0-flash"
DEFAULT_RESOURCE_NAME = "projects/local/locations/us-central1/publishers/google/models/gemini-2.0-flash"


def get_platform_client():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY is required")
    return genai.Client(api_key=api_key)


def get_platform_model_id():
    return os.getenv("GOOGLE_GENAI_MODEL_ID", DEFAULT_MODEL_ID)


def get_platform_resource_name():
    return os.getenv("GOOGLE_GENAI_RESOURCE_NAME", DEFAULT_RESOURCE_NAME)
