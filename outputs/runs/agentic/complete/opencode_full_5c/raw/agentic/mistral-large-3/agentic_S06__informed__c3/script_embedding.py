import os
from typing import List
import cohere


class ScriptEmbedder:
    """Embeds narration scripts for voice-asset search using Cohere Embed API."""

    def __init__(self):
        self.client = cohere.Client(os.getenv("COHERE_API_KEY"))

    def embed_script(self, text: str, model: str = "embed-english-v3.0") -> List[float]:
        """
        Embeds a narration script into a vector.

        Args:
            text: The text to embed.
            model: The embedding model to use (e.g., "embed-english-v3.0").

        Returns:
            List[float]: The embedding vector.

        Raises:
            cohere.CohereError: If the embedding fails.
        """
        response = self.client.embed(texts=[text], model=model)
        return response.embeddings[0]
