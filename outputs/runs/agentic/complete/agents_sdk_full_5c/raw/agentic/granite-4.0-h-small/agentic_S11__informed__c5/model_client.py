# model_client.py
# Managed Model Platform Workflow: local configuration and client helpers
# Provider: Azure OpenAI
import os
import json
from typing import Any, Dict

# Global configuration loaded from environment variables
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

openai.api_type = "azure"
openai.api_base = AZURE_ENDPOINT
openai.api_key = AZURE_API_KEY
openai.api_version = "2023-05-15"

def get_default_client() -> Any:
    """Return a reusable OpenAI client configured for Azure OpenAI."""
    return openai

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize request payload to match Azure OpenAI schema."""
    # Ensure payload matches expected format for chat completions
    normalized = {
        "model": AZURE_DEPLOYMENT,
        "messages": payload.get("messages", []),
    }
    # Add optional parameters
    if "max_tokens" in payload:
        normalized["max_tokens"] = payload["max_tokens"]
    if "temperature" in payload:
        normalized["temperature"] = payload["temperature"]
    return normalized

if __name__ == "__main__":
    # Example: show loaded configuration
    print({"endpoint": AZURE_ENDPOINT, "deployment": AZURE_DEPLOYMENT})
