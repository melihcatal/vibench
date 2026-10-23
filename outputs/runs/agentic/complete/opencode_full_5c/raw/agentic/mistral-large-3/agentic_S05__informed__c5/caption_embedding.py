import os
from typing import AsyncGenerator, Dict, Any, List
from google.generativeai import GenerativeModel


async def caption_embedding(
    transcript_chunks: AsyncGenerator[List[Dict[str, Any]], None],
) -> AsyncGenerator[Dict[str, Any], None]:
    """Embeds caption chunks for semantic meeting search using Google Gemini Embeddings."""
    model = GenerativeModel(model_name="models/embedding-001")

    async for chunk in transcript_chunks:
        texts = [item["transcript"] for item in chunk if item["is_final"]]
        if not texts:
            continue

        embeddings = []
        for text in texts:
            response = await model.embed_content(content=text)
            embeddings.append(response.embedding)

        yield {
            "embeddings": embeddings,
            "chunk_size": len(texts),
        }
