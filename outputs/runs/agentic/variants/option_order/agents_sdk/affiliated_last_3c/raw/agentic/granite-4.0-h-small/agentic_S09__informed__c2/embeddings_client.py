import os
import json
from ibm_watsonx_ai.services import EmbeddingsService
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class DirectEmbeddingsClient:
    """Local helper client that wraps IBM Slate/IBM WatsonX embeddings API.

    This class contains helpers for request transformation, error handling,
    and response normalization.
    """

    def __init__(self):
        # Read credentials from environment variables
        api_key = os.getenv('WATSONX_API_KEY')
        project_id = os.getenv('WATSONX_PROJECT_ID')
        if not api_key or not project_id:
            raise RuntimeError('Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables')

        self.authenticator = IAMAuthenticator(api_key)
        self.service = EmbeddingsService(
            authenticator=self.authenticator,
            project_id=project_id
        )
        self.service.set_service_url('https://api.watsonx.ibm.com')

    def embed(self, text: str) -> dict:
        """Generate a single embedding.","""        result = self.service.create_text_embedding(content=text)
        # Validate response
        if result is None or 'embedding' not in result:
            raise ValueError('Unexpected response from embeddings service')
        return result

    def embed_batch(self, texts: list[str]) -> dict:
        """Generate embeddings for a batch of texts.","""        result = self.service.create_text_batch_embedding(content=texts)
        # Valid response contains 'embeddings' key with list of vectors
        if result is None or 'embeddings' not in result:
            raise ValueError('Unexpected batch response from embeddings service')
        return result
