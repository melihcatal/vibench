import os
from typing import Literal
from model_client import ManagedModelClient

SERVICE = "azure_openai"


def resolve_resource(
    request_type: Literal["model", "deployment", "inference_profile"],
) -> str:
    """
    Resolve a provider‑specific Azure OpenAI resource ID.
    • model   – returns azure OpenAI model name (e.g., "gpt-35-turbo")
    • deployment – returns deployment name configured in environment
    • inference_profile – returns inference profile ID via client helper
    """
    client = ManagedModelClient()  # reads AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY
    if request_type == "model":
        return os.getenv("AZURE_OPENAI_MODEL")  # e.g., gpt-35-turbo
    if request_type == "deployment":
        return os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if request_type == "inference_profile":
        return client.get_inference_profile_id()  # returns provider‑specific profile ID
    raise ValueError(f"Unknown resource type: {request_type}")
