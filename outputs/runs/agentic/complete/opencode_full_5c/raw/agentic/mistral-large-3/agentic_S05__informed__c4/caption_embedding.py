import os
from typing import AsyncGenerator, List

from openai import OpenAI


class CaptionEmbedder:
    """Embed caption chunks for semantic meeting search using OpenAI Embeddings."""

    def __init__(self, model: str = "text-embedding-ada-002"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    async def embed_chunks(
        self, chunks: AsyncGenerator[List[str], None]
    ) -> AsyncGenerator[List[float], None]:
        """Embed caption chunks for semantic search."""
        async for chunk in chunks:
            text = " ".join(chunk)
            response = self.client.embeddings.create(input=text, model=self.model)
            yield response.data[0].embedding
