import os
from typing import Dict, Any, Optional
from openai import OpenAI


class SafetyClient:
    """Local configuration and client helper utilities for Text Content Safety."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the safety client.

        Args:
            api_key: OpenAI API key. If not provided, reads from OPENAI_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)

    def get_default_thresholds(self) -> Dict[str, float]:
        """Get default safety thresholds for different categories."""
        return {
            "hate": 0.8,
            "hate/threatening": 0.7,
            "harassment": 0.8,
            "harassment/threatening": 0.7,
            "self-harm": 0.9,
            "self-harm/intent": 0.8,
            "self-harm/instructions": 0.7,
            "sexual": 0.8,
            "sexual/minors": 0.6,
            "violence": 0.8,
            "violence/graphic": 0.7,
        }

    def get_category_mapping(self) -> Dict[str, str]:
        """Get human-readable descriptions for moderation categories."""
        return {
            "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
            "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
            "harassment": "Content that expresses, incites, or promotes harassing language towards any target.",
            "harassment/threatening": "Harassment content that also includes violence or serious harm towards any target.",
            "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
            "self-harm/intent": "Content where the speaker expresses that they are engaging or intend to engage in acts of self-harm.",
            "self-harm/instructions": "Content that encourages performing acts of self-harm, such as suicide or cutting, or gives instructions or advice on how to do so.",
            "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services.",
            "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
            "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
            "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
        }

    def normalize_moderation_result(self, result: Any) -> Dict[str, Any]:
        """Normalize OpenAI moderation result to a standard format."""
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

    def check_api_health(self) -> bool:
        """Check if the OpenAI API is accessible."""
        try:
            # Make a simple moderation call to check API health
            self.client.moderations.create(model="text-moderation-latest", input="Test")
            return True
        except Exception:
            return False
