import os
from typing import Dict, Optional

def resolve_model_resource(
    use_case: str,
    environment: Optional[str] = None,
) -> Dict[str, str]:
    """
    Resolves a Cohere model or deployment resource based on use case and environment.
    Returns a dictionary with model identifier and deployment details.
    """
    environment = environment or os.getenv("COHERE_ENVIRONMENT", "production")

    model_mapping = {
        "chat": {
            "production": "command-r-plus",
            "staging": "command-r",
            "development": "command-nightly",
        },
        "summarization": {
            "production": "command-r-plus",
            "staging": "command-r",
            "development": "command-nightly",
        },
        "embedding": {
            "production": "embed-english-v3.0",
            "staging": "embed-english-v2.0",
            "development": "embed-english-light-v3.0",
        },
    }

    if use_case not in model_mapping:
        raise ValueError(f"Unsupported use case: {use_case}")

    model_id = model_mapping[use_case][environment]
    return {
        "model_id": model_id,
        "environment": environment,
        "provider": "cohere",
    }