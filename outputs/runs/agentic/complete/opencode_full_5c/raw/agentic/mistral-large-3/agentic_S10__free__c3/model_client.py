from typing import Optional, Dict, Any
import os
from pydantic import BaseModel, Field
import httpx


class ModelConfig(BaseModel):
    api_key: str = Field(..., description="API key for the hosted LLM service")
    base_url: str = Field(
        "https://api.mistral.ai/v1", description="Base URL for the hosted LLM service"
    )
    model_family: str = Field("mistral", description="Model family identifier")
    model_id: str = Field(
        "mistral/mistral-large-latest", description="Concrete model identifier"
    )


def load_config() -> ModelConfig:
    """Load configuration from environment variables."""
    return ModelConfig(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
        base_url=os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1"),
        model_family=os.getenv("MISTRAL_MODEL_FAMILY", "mistral"),
        model_id=os.getenv("MISTRAL_MODEL_ID", "mistral/mistral-large-latest"),
    )


class LLMClient:
    """Client for interacting with the hosted LLM service."""

    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config if config else load_config()
        self.client = httpx.AsyncClient()

    async def generate(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """Generate a completion for the given prompt."""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.config.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        response = await self.client.post(
            f"{self.config.base_url}/chat/completions",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def stream(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000
    ) -> httpx.Response:
        """Stream completions for the given prompt."""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        payload = {
            "model": self.config.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        response = await self.client.post(
            f"{self.config.base_url}/chat/completions",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
