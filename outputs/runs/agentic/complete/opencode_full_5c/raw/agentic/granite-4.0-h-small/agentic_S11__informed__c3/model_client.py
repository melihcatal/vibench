# model_client.py
# HELPER: thin wrapper around provider SDKs/REST clients with automatic detection

import os
import json
from typing import Any, Dict

# Provider detection via environment variables
PROVIDERS = {
    "aws": {
        "module": "boto3",
        "client_class": "bedrock",
    },
    "azure_openai": {
        "module": "azure.ai.generativemodels",
        "client_class": "GenerativeModel",
    },
    "azure": {
        "module": "azure.ai.contentsafety",
        "client_class": "ContentSafetyClient",
    },
    "hf": {
        "module": "huggingface_hub",
        "client_class": "InferenceApi",
    },
    "gcp": {
        "module": "vertexai",
        "client_class": "generative_model",
    },
    "alibaba": {
        "module": "alibabacloud_dashscope",
        "client_class": "DashScope",
    },
}


def infer_provider_name() -> str:
    """Detect which managed‑model platform is configured based on env vars."""
    if "AWS_ACCESS_KEY_ID" in os.environ:
        return "aws"
    if "AZURE_OPENAI_ENDPOINT" in os.environ:
        return "azure_openai"
    if "AZURE_CONTENT_SAFETY_ENDPOINT" in os.environ:
        return "azure"
    if "HF_TOKEN" in os.environ:
        return "hf"
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        return "gcp"
    if "DASHSCOPE_API_KEY" in os.environ:
        return "alibaba"
    raise RuntimeError("No supported provider configured via environment variables")


def get_provider_client(provider_name: str = None) -> Any:
    """Return a low‑level client for the selected provider."""
    if provider_name is None:
        provider_name = infer_provider_name()
    spec = PROVIDERS.get(provider_name)
    if not spec:
        raise ValueError(f"Unsupported provider: {provider_name}")
    module = __import__(spec["module"], fromlist=[spec["client_class"]])
    client_cls = getattr(module, spec["client_class"])
    # Instantiate with the credentials implied by env vars (simplest form)
    return client_cls()


def normalize_request_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize payload to provider‑specific schema if needed."""
    # Example: Bedrock expects {'model': ..., 'input': {'text': ...}}
    if infer_provider_name() == "aws":
        return {
            "model": payload["model"],
            "input": {"text": payload["input"]},
        }
    # Placeholder for other providers’ normalisation logic
    return payload
