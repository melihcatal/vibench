import os
import asyncio
from typing import AsyncGenerator, Dict, Any, List
from ibm_watsonx_ai import APIClient


def embed_caption_chunks(
    transcript_stream: AsyncGenerator[Dict[str, Any], None],
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Embeds caption chunks for semantic meeting search using IBM watsonx.ai Slate embeddings.
    """
    watsonx_client = APIClient(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )

    async def batch_chunks():
        buffer = []
        async for chunk in transcript_stream:
            if chunk["type"] == "final":
                buffer.append(chunk["text"])
                if len(buffer) >= 5:
                    yield buffer
                    buffer = []
        if buffer:
            yield buffer

    async for batch in batch_chunks():
        embeddings = watsonx_client.text_embeddings.create(
            model_id="ibm/slate-125m-english-rtrvr", inputs=batch
        )

        for text, embedding in zip(batch, embeddings):
            yield {
                "text": text,
                "embedding": embedding,
                "model": "ibm/slate-125m-english-rtrvr",
            }
