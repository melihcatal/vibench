# Azure OpenAI Embeddings (service=Azure OpenAI embeddings; sdk=boto3 / Bedrock Runtime)
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BEDROCK_ENDPOINT environment variables required

import os
import boto3
import asyncio
from typing import AsyncIterable
from .speech_models import normalize_result

BEDROCK_ENDPOINT = os.getenv("BEDROCK_ENDPOINT")
BEDROCK_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
BEDROCK_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    endpoint_url=BEDROCK_ENDPOINT,
    aws_access_key_id=BEDROCK_ACCESS_KEY,
    aws_secret_access_key=BEDROCK_SECRET_KEY,
)


async def embed_captions(caption_chunks: AsyncIterable[str]):
    """Embed each caption chunk using Amazon Titan Embeddings (via Bedrock Runtime)."""
    # Define embedding model ID for Amazon Titan
    model_id = "amazon.titan-text-express-v1.0"
    async for caption in caption_chunks:
        # Call Bedrock Embeddings API
        response = bedrock_runtime.embed_content(
            contentType="text/plain", body=caption.encode("utf-8"), modelId=model_id
        )
        # Bedrock returns a binary payload, decode to JSON
        embedding = response["body"].read().decode("utf-8")
        # The API returns JSON like {"embeddings": [{"index": 0, "embedding": [...] }]
        embedding_data = json.loads(embedding)["embeddings"][0]["embedding"]
        print(f"Caption: {caption[:30]}... Embedding shape: {len(embedding_data)}")


async def demo():
    samples = ["First caption chunk...", "Second caption chunk with more content..."]

    async def gen():
        for s in samples:
            yield s
            await asyncio.sleep(0.1)

    await embed_captions(gen())


if __name__ == "__main__":
    asyncio.run(demo())
