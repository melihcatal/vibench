from typing import Dict, Any, Tuple
from model_models import ChatResponse


def collect_platform_metadata(response: ChatResponse) -> Dict[str, Any]:
    """
    Collects Azure AI Inference metadata from model response.
    Returns model output and platform metadata like usage and resource IDs.
    """
    metadata = {
        "model_output": response.content,
        "platform_metadata": {
            "id": response.id,
            "model": response.model,
            "usage": response.usage,
            "raw_response": response.raw_response,
        },
    }
    return metadata
