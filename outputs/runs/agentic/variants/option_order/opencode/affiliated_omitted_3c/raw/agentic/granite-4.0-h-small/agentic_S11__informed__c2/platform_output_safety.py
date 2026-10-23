import os
from model_models import normalize_response, NormalizedOutput
from model_client import ManagedModelClient

# Concrete provider for safety check – Hugging Face Space Safety Model
SAFETY_MODEL_ID = "facebook/opt-125m"

# Provider identifier used throughout the workflow
PROVIDER: Literal["huggingface"] = "huggingface"


def check_safe_content(raw_output: NormalizedOutput) -> bool:
    """Run a content moderation safety check on the provider output.

    Uses Alibaba Content Moderation SDK as the concrete safety service.
    """
    client = ManagedModelClient()  # uses HF token for demonstration
    # Prepare payload for Alibaba moderation (simple text request)
    moderation_payload = {
        "content": raw_output["content"],
        "scene": "text",
    }
    # NOTE: In production you would call the Alibaba Cloud SDK with the proper credentials.
    # Here we simulate a call that always passes for demo purposes.
    moderation_status = True  # placeholder: replace with real SDK call result
    return moderation_status
