"""
model_client.py - Local configuration and client helper utilities
for Hosted LLM Inference and Model-Family Selection.

Uses OpenAI as the concrete hosted LLM provider.
"""

import os
from typing import Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

# OpenAI provider configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_TIMEOUT = int(os.environ.get("OPENAI_TIMEOUT", "60"))
OPENAI_MAX_RETRIES = int(os.environ.get("OPENAI_MAX_RETRIES", "3"))

# Supported OpenAI model families
OPENAI_MODEL_FAMILIES = {
    "gpt-4o": "gpt-4o",
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4-turbo": "gpt-4-turbo",
    "o1": "o1",
    "o1-mini": "o1-mini",
}


def get_openai_client() -> OpenAI:
    """Create and return a configured OpenAI client instance."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        timeout=OPENAI_TIMEOUT,
        max_retries=OPENAI_MAX_RETRIES,
    )


def select_model(model_family: Optional[str] = None) -> str:
    """
    Select a concrete OpenAI model identifier based on the requested family.
    
    Args:
        model_family: One of the OPENAI_MODEL_FAMILIES keys, or None for default.
        
    Returns:
        A concrete OpenAI model identifier string.
    """
    if model_family is None or model_family not in OPENAI_MODEL_FAMILIES:
        return "gpt-4o"
    family = OPENAI_MODEL_FAMILIES[model_family]
    if family == "gpt-4o":
        return "gpt-4o-2024-08-06"
    elif family == "gpt-4o-mini":
        return "gpt-4o-mini-2024-07-18"
    elif family == "gpt-4-turbo":
        return "gpt-4-turbo-2024-04-09"
    elif family == "o1":
        return "o1-2024-12-17"
    elif family == "o1-mini":
        return "o1-mini-2024-09-12"
    return "gpt-4o-2024-08-06"


def build_chat_messages(
    system_prompt: str,
    user_content: str,
    format_instructions: Optional[str] = None,
) -> list[dict]:
    """Build a list of OpenAI chat messages from prompts."""
    messages = [{"role": "system", "content": system_prompt}]
    if format_instructions:
        user_content = f"{format_instructions}\n\n{user_content}"
    messages.append({"role": "user", "content": user_content})
    return messages


def extract_response_text(completion: ChatCompletion) -> str:
    """Extract the text content from an OpenAI ChatCompletion response."""
    if completion.choices and completion.choices[0].message:
        content = completion.choices[0].message.content
        return content if content else ""
    return ""


def extract_stream_text(chunk: ChatCompletionChunk) -> Optional[str]:
    """Extract text delta from an OpenAI streaming chunk."""
    if chunk.choices and chunk.choices[0].delta:
        delta = chunk.choices[0].delta.content
        return delta if delta else None
    return None
