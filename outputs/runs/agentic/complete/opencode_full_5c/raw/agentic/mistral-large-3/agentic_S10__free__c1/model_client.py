from typing import Optional, Dict, Any
import os
import httpx
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    api_key: str = Field(..., description="API key for the hosted LLM provider")
    base_url: str = Field(..., description="Base URL for the hosted LLM API")
    model_id: str = Field(
        ..., description="Default model identifier for the hosted LLM"
    )
    max_tokens: int = Field(
        default=1024, description="Maximum tokens for model responses"
    )
    temperature: float = Field(
        default=0.7, description="Temperature for model creativity"
    )


def load_config() -> ModelConfig:
    """Load configuration from environment variables."""
    return ModelConfig(
        api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        base_url="https://api.anthropic.com/v1/messages",
        model_id="claude-3-5-sonnet-20240620",
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "1024")),
        temperature=float(os.getenv("MODEL_TEMPERATURE", "0.7")),
    )


class LLMClient:
    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config if config else load_config()
        self.headers = {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    async def generate(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a completion from the hosted LLM."""
        payload = {
            "model": self.config.model_id,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config.base_url,
                json=payload,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def stream(self, prompt: str, system_prompt: Optional[str] = None):
        """Stream partial tokens from the hosted LLM."""
        payload = {
            "model": self.config.model_id,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": True,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                self.config.base_url,
                json=payload,
                headers=self.headers,
            ) as response:
                response.raise_for_status()
                async for chunk in response.aiter_text():
                    if chunk.strip():
                        yield chunk
