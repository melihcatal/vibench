import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class CaptionEmbedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    async def embed_text(self, text: str) -> list:
        response = self.client.embeddings.create(input=text, model=self.model)
        return response.data[0].embedding


async def embed_caption_chunks(caption_stream):
    embedder = CaptionEmbedder()
    async for caption in caption_stream:
        text = caption.get("text", "")
        embedding = await embedder.embed_text(text)
        yield {
            "text": text,
            "embedding": embedding,
            "type": caption.get("type", "interim"),
        }
