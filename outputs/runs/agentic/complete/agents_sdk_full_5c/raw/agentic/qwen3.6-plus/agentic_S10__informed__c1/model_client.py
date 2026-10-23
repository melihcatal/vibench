"""
Local configuration and client helper utilities for Hosted LLM Inference and Model-Family Selection.
Uses OpenAI as the concrete hosted LLM provider.
"""

import os
from typing import Optional, Dict, Any, List
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk


# Provider-specific environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Concrete OpenAI model identifiers
DEFAULT_MODEL = "gpt-4o"
FAST_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"


class OpenAIClient:
    """Wrapper around the OpenAI SDK client with configuration helpers."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.base_url = base_url or OPENAI_BASE_URL
        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        """Lazy-initialize the OpenAI SDK client."""
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return self._client

    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Retrieve metadata for a specific OpenAI model."""
        return {
            "model_id": model_id,
            "provider": "openai",
            "base_url": self.base_url,
        }

    def build_messages(
        self,
        system_prompt: str,
        user_prompt: str,
        context: Optional[str] = None,
        json_mode: bool = False,
    ) -> List[Dict[str, str]]:
        """Build a standardized message list for OpenAI chat completions."""
        messages = [{"role": "system", "content": system_prompt}]
        if context:
            messages.append({"role": "system", "content": f"Context:\n{context}"})
        messages.append({"role": "user", "content": user_prompt})
        return messages

    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
        stream: bool = False,
        response_format: Optional[Dict[str, str]] = None,
    ):
        """Create a chat completion using the OpenAI SDK."""
        kwargs: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        if json_mode or (response_format and response_format.get("type") == "json_object"):
            kwargs["response_format"] = {"type": "json_object"}
        elif response_format:
            kwargs["response_format"] = response_format
        return self.client.chat.completions.create(**kwargs)

    def create_streaming_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ):
        """Create a streaming chat completion using the OpenAI SDK."""
        return self.create_chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

    def create_embedding(
        self,
        text: str,
        model: str = EMBEDDING_MODEL,
    ):
        """Create an embedding using the OpenAI Embeddings API."""
        return self.client.embeddings.create(
            model=model,
            input=text,
        )


def get_client() -> OpenAIClient:
    """Return a configured OpenAI client instance."""
    return OpenAIClient()
