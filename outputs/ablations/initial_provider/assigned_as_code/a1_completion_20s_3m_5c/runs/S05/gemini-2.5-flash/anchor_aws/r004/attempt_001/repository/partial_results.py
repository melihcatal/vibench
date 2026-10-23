import asyncio

import boto3

from amazon_transcribe.client import TranscribeStreamingClient

async def partial_results(stream_output):
    async for event in stream_output:
        for result in event.transcript.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": not result.is_partial}
