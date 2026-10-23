# vision_client.py
"""Local helper utilities for Static Image and Visual Understanding integrations.

Provides centralized configuration, credentials handling, and simple wrapper functions around the concrete provider SDKs.
"""

import os
from typing import Dict, Any

# Helper dict to map feature name to provider-specific client function
PROVIDER_CLIENTS = {
    # Azure AI Vision SDK
    "azure": {
        "client_class": "azure.ai.vision.imageanalysis.ImageAnalysisClient",
        "kwargs": {
            "endpoint": os.getenv("AZURE_VISION_ENDPOINT"),
            "credential": "azure.ai.vision.imageanalysis.AzureKeyCredential",
            "key": os.getenv("AZURE_VISION_KEY"),
        },
    },
    # Google Cloud Vision SDK
    "google": {
        "client_class": "google.cloud.vision.ImageAnnotatorClient",
        "kwargs": {
            "from_service_account_json": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        },
    },
    # OpenAI Gemini (via chat endpoint) – no explicit client class needed
    "openai": {},
}


def get_provider_client(feature: str = "azure") -> Any:
    """Return an instantiated client for the requested feature/provider.

    Args:
        feature: Identifier of the provider (default 'azure').

    Returns:
        Instantiated client object ready to call.
    """
    spec = PROVIDER_CLIENTS.get(feature)
    if not spec:
        raise ValueError(f"Unsupported feature: {feature}")
    cls_path = spec["client_class"]
    kwargs = spec["kwargs"]
    # Dynamically import the class
    module_name, class_name = cls_path.rsplit(".", 1)
    module = __import__(module_name, fromlist=[class_name])
    client_cls = getattr(module, class_name)
    # Resolve credential argument separately if needed
    cred_key = list(kwargs.get("credential", "")) + [kwargs.get("key", "")]
    cred_value = os.getenv(cred_key[0]) if cred_key else None
    if cred_key:
        kwargs["credential"] = __import__(cred_key[1]).__dict__.get(
            cred_key[2], cred_value
        )
    # Instantiate and return
    return client_cls(**kwargs)
