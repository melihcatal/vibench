# Text Content Safety Client Configuration and Utilities
import os
from typing import List, Dict, Optional
from google.cloud import language_v1
from google.api_core.client_options import ClientOptions
from safety_models import (
    ModerationRequest,
    BatchModerationRequest,
    TextModerationResult,
    SafetyScore,
    normalize_scores,
)


class SafetyClient:
    def __init__(self):
        self.client = self._create_client()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")

    def _create_client(self) -> language_v1.LanguageServiceClient:
        """Create Google Cloud Natural Language API client."""
        client_options = ClientOptions(
            api_endpoint="language.googleapis.com"
        )
        return language_v1.LanguageServiceClient(client_options=client_options)

    def moderate_text(self, request: ModerationRequest) -> TextModerationResult:
        """Moderate text using Google Cloud Natural Language API."""
        document = language_v1.Document(
            content=request["text"], type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = self.client.moderate_text(
            request={"document": document}
        )
        
        scores = normalize_scores({
            "hate": response.moderation_categories.hate_score,
            "violence": response.moderation_categories.violence_score,
            "sexual": response.moderation_categories.sexual_score,
            "harassment": response.moderation_categories.harassment_score,
            "dangerous": response.moderation_categories.dangerous_score,
        })
        
        flagged_categories = [
            score.category for score in scores if score.score > 0.5
        ]
        
        return TextModerationResult(
            blocked=len(flagged_categories) > 0,
            scores=scores,
            flagged_categories=flagged_categories,
        )

    def moderate_batch(self, request: BatchModerationRequest) -> List[TextModerationResult]:
        """Moderate a batch of texts."""
        return [self.moderate_text({"text": text}) for text in request["texts"]]