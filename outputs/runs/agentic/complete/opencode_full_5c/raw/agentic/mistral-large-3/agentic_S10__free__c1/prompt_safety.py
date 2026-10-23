from typing import Dict, Any, Optional
import os
import httpx
from pydantic import BaseModel, Field


class SafetyConfig(BaseModel):
    api_key: str = Field(..., description="API key for the safety moderation service")
    base_url: str = Field(
        default="https://api.openai.com/v1/moderations",
        description="Base URL for the safety moderation API",
    )


def load_safety_config() -> SafetyConfig:
    """Load safety moderation configuration from environment variables."""
    return SafetyConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
    )


class SafetyClient:
    def __init__(self, config: Optional[SafetyConfig] = None):
        self.config = config if config else load_safety_config()
        self.headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

    async def check_prompt(self, text: str) -> Dict[str, Any]:
        """Check if a prompt contains unsafe content using OpenAI's moderation API."""
        payload = {"input": text}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config.base_url,
                json=payload,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def check_generated_text(self, text: str) -> Dict[str, Any]:
        """Check if generated text contains unsafe content using OpenAI's moderation API."""
        return await self.check_prompt(text)
