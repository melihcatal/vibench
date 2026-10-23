from typing import AsyncIterator

import boto3

from speech_models import TranscriptChunk


async def stream_chunks(source: AsyncIterator[bytes]):
    boto3.client("transcribe", region_name="us-east-1")
    async for chunk in source:
        if chunk:
            yield TranscriptChunk(text=chunk.decode("utf-8", errors="ignore"), is_final=False)
