from typing import List


def select_cohere_model(
    available_models: List[str], desired_capability: str = "chat"
) -> str:
    """
    Selects a Cohere model based on a desired capability.

    This is a simplified placeholder. A real implementation might query an API
    or a local cache of model metadata.
    """
    # In a real scenario, this could involve more complex logic,
    # like checking model metadata for capabilities.
    # For this example, we'll use a simple mapping.

    model_map = {
        "chat": "command-r",
        "embed": "embed-english-v3.0",
        "rerank": "rerank-english-v2.0",
    }

    return model_map.get(desired_capability, "command-r")
