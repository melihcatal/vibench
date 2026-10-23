import os
from typing import Optional

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings


class WatsonXEmbeddingsClient:
    """Client for IBM WatsonX.ai embeddings service."""

    def __init__(self, api_key: Optional[str] = None, project_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("WATSONX_API_KEY")
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
        self.credentials = Credentials(self.api_key)
        self.client = Embeddings(credentials=self.credentials, project_id=self.project_id)

    def get_client(self) -> Embeddings:
        return self.client