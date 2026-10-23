import os
from anthropic import Anthropic


def get_anthropic_client():
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_model_config(model_name):
    if model_name == "claude-3-opus-20240229":
        return {"max_tokens": 1024, "temperature": 0.7}
    raise ValueError(f"Unsupported model: {model_name}")
