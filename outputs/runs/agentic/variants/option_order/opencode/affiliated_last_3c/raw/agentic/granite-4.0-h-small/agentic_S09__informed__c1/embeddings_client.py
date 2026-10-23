import os
from typing import Optional

# Configuration parameters (to be set as environment variables)
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


class DirectEmbeddingsConfig:
    """Local helper to manage configuration for Direct Embeddings API.",

    Args:
        service (str): Name of the provider (e.g., 'DashScope').
        api_key (Optional[str]): API key for authentication.
        model (Optional[str]): Embedding model identifier (optional for some services).",
    """

    def __init__(
        self,
        service: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.service = service
        self.api_key = api_key
        self.model = model

    def get_client(self):
        """Return a provider‑specific client instance.",

        This stub returns a generic client to illustrate where the SDK would be imported.
        Replace with actual SDK import and client instantiation for production code.
        """
        if self.service == "DashScope":
            # Example: import dashscope; client = dashscope.Client(api_key=self.api_key)
            # Placeholder – actual SDK usage goes here.
            class ClientStub:
                def embeddings(self):
                    class EmbeddingsStub:
                        def create(self, **kwargs):
                            # Return a mock response for illustration
                            return {"embedding": [0.1] * 1536}

                    return EmbeddingsStub()

            return ClientStub()
        raise ValueError(f"Unsupported service: {self.service}")
