import os
from typing import Optional
from google.cloud import language_v1
from safety_models import TextModerationRequest, ModerationResult, BatchModerationResult


class SafetyClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required.")
        self.client = language_v1.LanguageServiceClient()

    def analyze_text(self, request: TextModerationRequest) -> ModerationResult:
        document = language_v1.Document(
            content=request["text"],
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language=request.get("language", "en")
        )
        response = self.client.moderate_text(document=document)

        categories = {
            "toxic": response.moderation_categories.toxicity_score > 0.5,
            "insult": response.moderation_categories.insult_score > 0.5,
            "profanity": response.moderation_categories.profanity_score > 0.5,
            "derogatory": response.moderation_categories.derogatory_score > 0.5,
            "sexual": response.moderation_categories.sexual_score > 0.5,
            "violent": response.moderation_categories.violence_score > 0.5,
        }
        category_scores = {
            "toxic": response.moderation_categories.toxicity_score,
            "insult": response.moderation_categories.insult_score,
            "profanity": response.moderation_categories.profanity_score,
            "derogatory": response.moderation_categories.derogatory_score,
            "sexual": response.moderation_categories.sexual_score,
            "violent": response.moderation_categories.violence_score,
        }

        return ModerationResult(
            flagged=any(categories.values()),
            categories=categories,
            category_scores=category_scores
        )