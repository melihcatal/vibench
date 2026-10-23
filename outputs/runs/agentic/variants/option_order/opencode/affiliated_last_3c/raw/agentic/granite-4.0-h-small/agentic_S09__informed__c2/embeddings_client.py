import os
import dashscope
from dotenv import load_dotenv

load_dotenv()

# Provider: DashScope

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise RuntimeError("Set DASHSCOPE_API_KEY env var")


class EmbeddingsClient:
    """Local helper client for DashScope Embeddings API."""

    def __init__(self):
        self.client = dashscope.Embeddings(api_key=DASHSCOPE_API_KEY)

    def embed(self, text: str) -> list:
        """Generate embedding for a single text. Returns list of floats."""
        response = self.client.embed(text=text)
        return response["embeddings"][0]

    def embed_batch(self, texts: list) -> list:
        """Batch embed multiple texts."""
        response = self.client.embed_batch(texts=texts)
        # Assuming each element contains a list of embeddings under 'embeddings'
        return [item["embeddings"][0] for item in response]
