# Moderate a Batch of User Messages
from typing import List
from safety_client import SafetyClient
from safety_models import BatchModerationRequest, TextModerationResult


class BatchModerator:
    def __init__(self):
        self.client = SafetyClient()

    def moderate_batch(self, texts: List[str]) -> List[TextModerationResult]:
        """Moderate a batch of texts using Google Cloud Natural Language API."""
        request: BatchModerationRequest = {"texts": texts}
        return self.client.moderate_batch(request)