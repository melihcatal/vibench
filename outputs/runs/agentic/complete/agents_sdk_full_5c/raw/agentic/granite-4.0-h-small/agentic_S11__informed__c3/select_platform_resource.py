# select_platform_resource.py
# Same-scenario scored file: resolve a provider-specific model, deployment, or inference resource before invocation

import os
from typing import Optional, Dict

# Vertex AI: resolve model name based on desired family and deployment
# Example: using "gemini-1.5-flash" as the model ID (resource identifier)
MODEL_FAMILY = os.getenv("MODEL_FAMILY", "gemini-1.5-flash")


def select_resource(deployment: Optional[str] = None) -> str:
    """
    Select the appropriate Vertex AI model resource identifier.

    Args:
        deployment (Optional[str]): Optional deployment name to further scope the model.

    Returns:
        str: Model identifier string to be used with invoke_model().
    """
    # In a real deployment the deployment name could be fetched from a config service.
    # Here we simply return the model family name, which is the resource identifier for
    # Vertex AI generative models.
    return MODEL_FAMILY

if __name__ == "__main__":
    resource = select_resource()
    print("Selected Vertex AI resource:", resource)
