import os
from typing import Optional

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Embeddings


class EmbeddingsClient:
    """Client for IBM Slate Embeddings via watsonx.ai."""

    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.client: Optional[APIClient] = None
        self.embeddings_model: Optional[Embeddings] = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the WatsonX AI client and embeddings model."""
        if not self.api_key or not self.project_id:
            raise ValueError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be set.")

        self.client = APIClient(api_key=self.api_key, url=self.url)
        self.client.set_project_id(self.project_id)

        self.embeddings_model = Embeddings(
            model_id="ibm/slate.125m.english.rtrvr", client=self.client
        )

    def get_client(self) -> APIClient:
        """Return the WatsonX AI client."""
        if not self.client:
            raise ValueError("Client not initialized.")
        return self.client

    def get_embeddings_model(self) -> Embeddings:
        """Return the embeddings model."""
        if not self.embeddings_model:
            raise ValueError("Embeddings model not initialized.")
        return self.embeddings_model
