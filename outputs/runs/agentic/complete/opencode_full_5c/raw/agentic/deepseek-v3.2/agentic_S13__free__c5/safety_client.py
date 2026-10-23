import os
from typing import Dict, Any, Optional
from openai import OpenAI


class SafetyClient:
    """Provide local configuration and client helper utilities for Text Content Safety."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=self.api_key)
        self.moderation_model = "text-moderation-latest"

    def get_moderation_client(self) -> OpenAI:
        """Get the OpenAI client instance."""
        return self.client

    def get_moderation_model(self) -> str:
        """Get the moderation model identifier."""
        return self.moderation_model

    def validate_text(self, text: str) -> bool:
        """Validate text is not empty and within reasonable length."""
        if not text or not isinstance(text, str):
            return False
        if len(text) > 10000:
            return False
        return True

    def prepare_moderation_request(self, text: str) -> Dict[str, Any]:
        """Prepare a moderation request payload."""
        return {"model": self.moderation_model, "input": text}

    def parse_moderation_response(self, response) -> Dict[str, Any]:
        """Parse OpenAI moderation response into a standardized format."""
        result = response.results[0]
        return {
            "flagged": result.flagged,
            "categories": result.categories.model_dump(),
            "category_scores": result.category_scores.model_dump(),
        }

    @staticmethod
    def get_default_thresholds() -> Dict[str, float]:
        """Get default safety thresholds for different categories."""
        return {
            "harassment": 0.8,
            "hate": 0.8,
            "self-harm": 0.7,
            "sexual": 0.8,
            "violence": 0.8,
            "harassment/threatening": 0.9,
            "hate/threatening": 0.9,
            "self-harm/intent": 0.6,
            "self-harm/instructions": 0.6,
            "sexual/minors": 0.7,
            "violence/graphic": 0.8,
        }
