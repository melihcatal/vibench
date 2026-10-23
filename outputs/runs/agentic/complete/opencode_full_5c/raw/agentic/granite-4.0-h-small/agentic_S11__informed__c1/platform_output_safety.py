# [LATER-STEP] platform_output_safety.py
# Check platform model output for unsafe content (e.g., toxicity, hate, self‑harm)

from model_client import ManagedModelClient
from model_models import ProviderResponse


def is_output_safe(output_content: str) -> bool:
    """
    Run the output through a provider‑specific content‑safety service.
    For this example we use Azure AI Content Safety (rest interface).
    """
    client = ManagedModelClient()
    # Prepare payload for Content Safety endpoint
    safety_payload = {
        "content": output_content,
        "category": ["text"],
        "moderationLevel": "strict",
    }
    # NOTE: In a real implementation you would call the Azure Content Safety REST API
    # here. For illustration we call a dummy SDK method that mimics the response.
    safety_response = client.content_safety.detect_text(**safety_payload)
    return safety_response["flagged"] == False
