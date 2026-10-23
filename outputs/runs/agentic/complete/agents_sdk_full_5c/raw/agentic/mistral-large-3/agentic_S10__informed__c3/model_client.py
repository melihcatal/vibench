import os
from typing import Optional
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def get_mistral_client() -> MistralClient:
    """
    Initialize and return a Mistral client using the API key from environment.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set")
    return MistralClient(api_key=api_key)


def validate_model(model: str) -> bool:
    """
    Validate if the model is supported by Mistral.
    """
    supported_models = {
        "mistral-tiny",
        "mistral-small", 
        "mistral-medium",
        "mistral-large-latest"
    }
    return model in supported_models