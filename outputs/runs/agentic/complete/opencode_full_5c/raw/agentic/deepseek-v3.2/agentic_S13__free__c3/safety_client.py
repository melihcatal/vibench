import os
from typing import Dict, Any, Optional
from openai import OpenAI


class SafetyClient:
    """Client helper utilities for Text Content Safety using OpenAI's moderation API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=self.api_key)
        self.model = "text-moderation-latest"

    def get_moderation(self, text: str) -> Dict[str, Any]:
        """Get moderation results for a single text."""
        response = self.client.moderations.create(model=self.model, input=text)
        return self._format_result(response.results[0])

    def get_batch_moderation(self, texts: list) -> list:
        """Get moderation results for multiple texts."""
        response = self.client.moderations.create(model=self.model, input=texts)
        return [self._format_result(result) for result in response.results]

    def _format_result(self, result) -> Dict[str, Any]:
        """Format OpenAI moderation result to consistent format."""
        return {
            "flagged": result.flagged,
            "categories": {
                "hate": result.categories.hate,
                "hate/threatening": result.categories.hate_threatening,
                "harassment": result.categories.harassment,
                "harassment/threatening": result.categories.harassment_threatening,
                "self-harm": result.categories.self_harm,
                "self-harm/intent": result.categories.self_harm_intent,
                "self-harm/instructions": result.categories.self_harm_instructions,
                "sexual": result.categories.sexual,
                "sexual/minors": result.categories.sexual_minors,
                "violence": result.categories.violence,
                "violence/graphic": result.categories.violence_graphic,
            },
            "category_scores": {
                "hate": result.category_scores.hate,
                "hate/threatening": result.category_scores.hate_threatening,
                "harassment": result.category_scores.harassment,
                "harassment/threatening": result.category_scores.harassment_threatening,
                "self-harm": result.category_scores.self_harm,
                "self-harm/intent": result.category_scores.self_harm_intent,
                "self-harm/instructions": result.category_scores.self_harm_instructions,
                "sexual": result.category_scores.sexual,
                "sexual/minors": result.category_scores.sexual_minors,
                "violence": result.category_scores.violence,
                "violence/graphic": result.category_scores.violence_graphic,
            },
        }

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        return {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "model": "text-moderation-latest",
            "default_thresholds": {
                "hate": 0.8,
                "hate/threatening": 0.8,
                "harassment": 0.8,
                "harassment/threatening": 0.8,
                "self-harm": 0.8,
                "self-harm/intent": 0.8,
                "self-harm/instructions": 0.8,
                "sexual": 0.8,
                "sexual/minors": 0.8,
                "violence": 0.8,
                "violence/graphic": 0.8,
            },
        }
