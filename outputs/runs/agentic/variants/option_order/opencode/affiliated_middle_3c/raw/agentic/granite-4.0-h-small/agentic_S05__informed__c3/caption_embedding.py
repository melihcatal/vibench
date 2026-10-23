import os
import asyncio
from google.cloud import genai

class CaptionEmbedding:
    """
    Embeds caption chunks for semantic meeting search using Gemini Embeddings.
    Provider: Gemini Embeddings (service=Google Gemini API)
    Configuration:
        GOOGLE_API_KEY must be set in the environment.
    """

    def __init__(self, model: str = "gemini-1.5-flash"),
    """
        Initializes the embedding client.
    """
        if not os.getenv("GOOGLE_API_KEY"):
            raise RuntimeError("GOOGLE_API_KEY environment variable not set")
        # Google AI client uses the GOOGLE_API_KEY env var directly
        self.embedder = genai.Embedding(model)

    async def embed_stream(self, text_stream):
        """Embed each text chunk and yield embedding vector."""
        for chunk in text_stream:
            embedding = self.embedder.embed(chunk)
            yield {
                "text": chunk,
                "embedding": embedding.embedding,
            }

if __name__ == "__main__":
    # Example usage with a dummy generator
    async def dummy_stream():
        for i in range(3):
            yield f"Meeting discussion point {i}"

    embedder = CaptionEmbedding()
    asyncio.run(embedder.embed_stream(dummy_stream()))