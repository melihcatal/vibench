import os
from typing import Optional, Dict, Any
from openai import OpenAI
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuration for hosted LLM models."""

    provider: str = "openai"
    api_key_env_var: str = "OPENAI_API_KEY"
    default_model: str = "gpt-3.5-turbo"
    temperature: float = 0.3
    max_tokens: int = 500
    timeout: int = 30


class ModelClient:
    """Client helper for hosted LLM inference."""

    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config or ModelConfig()
        self.api_key = os.environ.get(self.config.api_key_env_var)

        if not self.api_key:
            raise ValueError(
                f"API key not found in environment variable {self.config.api_key_env_var}"
            )

        if self.config.provider == "openai":
            self.client = OpenAI(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    def create_completion(self, prompt: str, **kwargs) -> str:
        """Create a completion using the configured model."""
        model = kwargs.get("model", self.config.default_model)
        temperature = kwargs.get("temperature", self.config.temperature)
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    def create_chat_completion(self, messages: list, **kwargs) -> str:
        """Create a chat completion with custom messages."""
        model = kwargs.get("model", self.config.default_model)
        temperature = kwargs.get("temperature", self.config.temperature)
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    def stream_completion(self, prompt: str, **kwargs):
        """Stream completion tokens."""
        model = kwargs.get("model", self.config.default_model)
        temperature = kwargs.get("temperature", self.config.temperature)
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)

        stream = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


def get_model_client(provider: str = "openai") -> ModelClient:
    """Factory function to get a model client for a specific provider."""
    if provider == "openai":
        config = ModelConfig(
            provider="openai",
            api_key_env_var="OPENAI_API_KEY",
            default_model="gpt-3.5-turbo",
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    return ModelClient(config)
