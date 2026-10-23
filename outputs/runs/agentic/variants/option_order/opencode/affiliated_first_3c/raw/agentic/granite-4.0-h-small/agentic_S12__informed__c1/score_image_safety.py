# Check an image for unsafe or policy-sensitive visual content using watsonx guardrails
import os
import ibm_watsonx_ai
from ibm_watsonx_ai.hap_guard import HapGuardClient
from vision_client import get_watsonx_client
from vision_models import is_unsafe

# Configure watsonx client as a singleton
WATSONX_CLIENT = get_watsonx_client()
GUARD_CLIENT = HapGuardClient(watsonx_client=WATSONX_CLIENT)


def score_image_safety(image_path: str):
    """Check an image for unsafe content and return a boolean indicating safety."""
    # Load image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    # Call watsonx guardrails API
    result = GUARD_CLIENT.analyze(image_bytes=image_bytes, content_type="image/jpeg")
    # Guardrails returns a safety score; treat score < 0.5 as unsafe
    unsafe = result["safety_score"] < 0.5
    return not unsafe  # Return True if safe
