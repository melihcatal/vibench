import os


def init_model_client(provider: str, **kwargs) -> object:
    """Initialize a provider-specific client helper.
    Returns a minimal wrapper object exposing an `invoke(prompt, **extra)` method.
    The concrete client implementation lives in separate helper modules that should be imported here.
    """
    if provider == "Hugging Face":
        from .model_clients.hf_client import HFClient

        return HFClient(token=os.getenv("HF_TOKEN"), **kwargs)
    elif provider == "Amazon Bedrock":
        from .model_clients.bedrock_client import BedrockClient

        return BedrockClient(
            region=kwargs.get("region", "us-east-1"),
            credentials=kwargs.get("credentials", None),
        )
    elif provider == "Vertex AI":
        from .model_clients.vertex_client import VertexClient

        return VertexClient(
            project=kwargs.get("project", "auto"),
            location=kwargs.get("location", "us-central1"),
        )
    else:
        raise ValueError(f"Unsupported provider for client init: {provider}")
