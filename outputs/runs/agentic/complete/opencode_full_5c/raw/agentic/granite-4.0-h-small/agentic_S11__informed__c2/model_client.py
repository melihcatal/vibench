# [HELPER] model_client.py

# Local configuration & client helper utilities for Managed Model Platform Workflow
import os
from typing import Dict, Any

# ----------- Provider selection -----------
# Set the desired provider via environment variable (default = AWS Bedrock)
PROVIDER = os.getenv("MODEL_PLATFORM", "bedrock")

# ----------- Common helpers -----------


def load_credentials() -> Dict[str, str]:
    """Load credentials for the selected provider."""
    creds = {}
    if PROVIDER == "bedrock":
        creds["access_key"] = os.getenv("AWS_ACCESS_KEY_ID")
        creds["secret_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")
        creds["region"] = os.getenv("AWS_REGION", "us-east-1")
    elif PROVIDER == "huggingface":
        creds["hf_token"] = os.getenv("HF_TOKEN")
    elif PROVIDER == "vertexai":
        creds["project_id"] = os.getenv("GOOGLE_CLOUD_PROJECT")
        creds["credentials_path"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")
    return creds


def get_client() -> Any:
    """Return a configured client instance for the chosen provider."""
    creds = load_credentials()
    if PROVIDER == "bedrock":
        import boto3

        return boto3.client(
            "bedrock",
            region_name=creds["region"],
            aws_access_key_id=creds["access_key"],
            aws_secret_access_key=creds["secret_key"],
        )
    elif PROVIDER == "huggingface":
        from huggingface_hub import InferenceApi

        return InferenceApi(token=creds["hf_token"])
    elif PROVIDER == "vertexai":
        from vertexai.preview.language_models import TextGenerationModel

        # Requires GOOGLE_APPLICATION_CREDENTIALS env variable
        return TextGenerationModel.from_pretrained("gemini-1.5-flash")
    else:
        raise NotImplementedError(f"Client for provider {PROVIDER} not implemented")
