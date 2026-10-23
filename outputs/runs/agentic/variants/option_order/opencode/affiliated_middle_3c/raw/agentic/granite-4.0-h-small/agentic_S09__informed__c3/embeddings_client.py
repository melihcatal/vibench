import os

#
# Local helper utilities for Direct Embeddings API integration
#


class EmbedderClient:
    """Simple client wrapper to interact with a hosted embeddings provider."

    This class abstracts provider selection, API key handling, and request/response basics.
    Currently it uses the OpenAI SDK as the concrete provider.
    """

    def __init__(self):
        # Read the provider-specific API key from environment variables.
        self.api_key = os.getenv("OPENAI_API_KEY", "dummy_key")
        # Base client – placeholder for real SDK import in production.
        # from openai import OpenAI
        # self._client = OpenAI(api_key=self.api_key)
        # For this script we only need a thin wrapper that records the selected provider.
        self.provider = None

    def set_provider(self, provider_name: str):
        """Record which provider is being used."""
        self.provider = provider_name

    def embed(self, text: str) -> list[float]:
        """Generate a single embedding (stub implementation)."""
        # TODO: Replace with real call to self._client.embeddings.create(...)
        # Here we return a mock vector of the same length as OpenAI's 1536-dim embedding.
        mock_vector = [0.01 * i for i in range(1536)]
        return mock_vector

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Batch embedding (stub implementation)."""
        # Return a list of mock vectors, one per input text.
        return [[0.01 * i for i in range(1536)] for _ in texts]

    def close(self):
        """Clean up resources if needed."""
        pass
