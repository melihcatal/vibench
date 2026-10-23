# [HELPER] vision_client.py
# Centralized helper utilities for static image and visual understanding providers
import os
from typing import Any, Dict

# ----- Google Cloud Vision ----- #
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError(
        "Set GOOGLE_APPLICATION_CREDENTIALS to point to a service account JSON"
    )

# ----- Amazon Rekognition ----- #
# Credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are learned from environment by boto3

# ----- Azure AI Vision ----- #
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
if not AZURE_VISION_ENDPOINT:
    raise RuntimeError("Set AZURE_VISION_ENDPOINT environment variable")
AZURE_VISION_CREDENTIAL = os.getenv(
    "AZURE_VISION_KEY"
)  # optional, DefaultAzureCredential will try env/managed identity

# ----- Azure AI Image Analysis ----- #
AZURE_IMAGE_ANALYSIS_ENDPOINT = os.getenv("AZURE_IMAGE_ANALYSIS_ENDPOINT")
AZURE_IMAGE_ANALYSIS_CREDENTIAL = os.getenv("AZURE_IMAGE_ANALYSIS_KEY")

# ----- IBM watsonx HAP guardrails (safety) ----- #
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
if not (WATSONX_API_KEY and WATSONX_PROJECT_ID):
    raise RuntimeError(
        "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
    )


# ----- Generic helpers ----- #
def load_env_vars(required: Dict[str, str]) -> None:
    """Validate that all required environment variables are present."""
    missing = [k for k, v in required.items() if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")


# Example usage in a helper function
# load_env_vars({"Google": "GOOGLE_APPLICATION_CREDENTIALS", "Azure": "AZURE_VISION_ENDPOINT"})
