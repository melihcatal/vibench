import os
from typing import Literal

# Define supported service identifiers and their associated model IDs
Service = Literal["dashscope", "openai", "gemini", "cohere", "ibm"]

def service_to_model(service: Service) -> str:
    """Map a service name to the corresponding model identifier."""
    mapping = {
        "dashscope": "text-embedding-ada-002",  # generic Ada-002 style
        "openai": "text-embedding-ada-002",
        "gemini": "gemini-1.5-pro-embedding",
        "cohere": "cohere-embedding-v1",
        "ibm": "ibm-embedding-v2",
    }
    return mapping.get(service.lower(), "text-embedding-ada-002")

# Example configuration - in real use these could be read from env vars or a config file
DEFAULT_SERVICE: Service = "dashscope"
DEFAULT_MODEL: str = service_to_model(DEFAULT_SERVICE)


def get_model_for_service(service: Service) -> str:
    """Retrieve the model identifier for a given service."""
    return service_to_model(service)
