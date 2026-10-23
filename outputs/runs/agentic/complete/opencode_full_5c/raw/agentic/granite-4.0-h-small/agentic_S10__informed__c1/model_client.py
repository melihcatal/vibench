# Local helper utilities for hosted LLM inference and model family selection
import os
from typing import Any, Dict, Optional

# Example: select client implementation based on environment variables or config


def get_text_chat_client(model_family: str = "granite-4") -> Any:
    """
    Return a configured LLM client instance for text chat.

    Args:
        model_family: Identifier for the hosted model (e.g., "granite-4", "qwen", "mistral").

    Returns: An object exposing a `chat` method compatible with OpenAI‑style SDKs.
    """
    # Placeholder logic – map the identifier to an actual SDK call
    if model_family == "granite-4":
        # IBM watsonx.ai (requires env vars WATSONX_API_KEY, WATSONX_PROJECT_ID)
        from ibm_watsonx_ai.clients import GraniteClient

        return GraniteClient()  # Exposes .chat(...)
    elif model_family == "qwen":
        # Alibaba / DashScope Qwen API (requires DASHSCOPE_API_KEY)
        from dashscope.apis import ChatCompletion

        return ChatCompletion()
    elif model_family == "mistral":
        # Mistral AI chat API (requires MISTRAL_API_KEY)
        from mistralai.models.chat.completions import ChatCompletion as MistralChat

        return MistralChat()
    elif model_family == "anthropic":
        # Anthropic Messages API (requires ANTHROPIC_API_KEY)
        import anthropic

        client = anthropic.Anthropic()
        return client.messages.create
    elif model_family == "gemini":
        # Google Gemini API (requires GOOGLE_API_KEY)
        from google.generativeai import generate

        return generate
    elif model_family == "bedrock":
        # Amazon Bedrock Runtime (requires AWS credentials)
        import boto3

        return boto3.client("bedrock-runtime")
    elif model_family == "openai":
        # OpenAI Chat Completions (requires OPENAI_API_KEY)
        import openai

        return openai.ChatCompletion.create
    else:
        raise ValueError(f"Unsupported model_family: {model_family}")


def normalize_response(resp: Any) -> Dict[str, Any]:
    """
    Normalize disparate LLM responses to a common dict shape.
    """
    if isinstance(resp, dict):
        # Assume openai‑style or Watson X style with .choices
        choices = resp.get("choices", [{}])[0]
        return {
            "role": choices.get("role", "assistant"),
            "content": choices.get("message", {}).get("content", ""),
        }
    # If the SDK already returns a string, wrap it
    return {"role": "assistant", "content": str(resp)}


#
# Example usage (uncomment to test):
#
# client = get_text_chat_client("bedrock")
# raw = client(
#     prompt="Summarize the following:\n\"...\"",
#     max_tokens=150,
# )
# normalized = normalize_response(raw)
# print(normalized)
