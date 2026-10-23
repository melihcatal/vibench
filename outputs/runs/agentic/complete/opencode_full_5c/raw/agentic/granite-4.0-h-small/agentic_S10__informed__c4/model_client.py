import os
from typing import Dict, Any

# Provider configuration section – fill in the appropriate credentials before running

# Example: Anthropic (Messages API)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Example: OpenAI (Chat Completion)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Example: Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Example: Amazon Bedrock (Nova/Titan)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BEDROCK_ENDPOINT = os.getenv(
    "BEDROCK_ENDPOINT"
)  # e.g. https://bedrock.us-east-1.amazonaws.com

# Example: watsonx (Granite)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Example: DashScope Qwen
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


# Helper to select credentials based on desired provider
def get_provider_config(provider: str) -> Dict[str, Any]:
    """Return a dict of credentials/configuration for the chosen provider.
    Providers must have their env variables defined as shown above.
    """
    config = {}
    if provider == "anthropic":
        config.update(
            {
                "api_key": ANTHROPIC_API_KEY,
                "endpoint": "https://api.anthropic.com/v1/messages",
            }
        )
    elif provider == "openai":
        config.update(
            {
                "api_key": OPENAI_API_KEY,
                "endpoint": "https://api.openai.com/v1/chat/completions",
            }
        )
    elif provider == "google":
        config.update(
            {
                "api_key": GOOGLE_API_KEY,
                "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-001:generateContent",
            }
        )
    elif provider == "bedrock":
        config.update(
            {
                "api_key": AWS_SECRET_ACCESS_KEY,
                "endpoint": BEDROCK_ENDPOINT,
            }
        )
    elif provider == "watsonx":
        config.update(
            {
                "api_key": WATSONX_API_KEY,
                "project_id": WATSONX_PROJECT_ID,
                "endpoint": "https://api.us-south.watsonx.ibm.com/v1/text/chat/generate",
            }
        )
    elif provider == "dashscope":
        config.update(
            {
                "api_key": DASHSCOPE_API_KEY,
                "endpoint": "https://api.dashscope.ai/v1/chat/completions",
            }
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    return config


def normalize_response(resp: Dict[str, Any], provider: str) -> Dict[str, Any]:
    """Normalize the raw response from the provider to a common shape.
    Returns a dict with keys: 'text' (or 'content'), 'usage', 'model'.
    """
    if provider == "anthropic":
        return {
            "text": resp.get("content", [{}])[0].get("text"),
            "usage": resp.get("usage"),
            "model": resp.get("model"),
        }
    elif provider == "openai":
        return {
            "text": resp.get("choices", [{}])[0].get("message", {}).get("content"),
            "usage": resp.get("usage"),
            "model": resp.get("model"),
        }
    elif provider == "google":
        return {
            "text": resp.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text"),
            "usage": None,
            "model": "gemini-1.5-pro-001",
        }
    elif provider == "bedrock":
        return {
            "text": resp.get("body", {}).get("contentItems", [{}])[0].get("text"),
            "usage": None,
            "model": "nova-2024-04",
        }
    elif provider == "watsonx":
        return {
            "text": resp.get("result", {}).get("output", {}).get("text"),
            "usage": None,
            "model": resp.get("model"),
        }
    elif provider == "dashscope":
        return {
            "text": resp.get("choice", [{}])[0].get("message", {}).get("content"),
            "usage": None,
            "model": resp.get("model"),
        }
    raise ValueError(f"No normalizer for provider: {provider}")
