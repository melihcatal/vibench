import asyncio
# Alibaba Cloud MQTT (or equivalent) streaming integration for speech chunks
# SDK: alibabacloud_alimt / alibabacloud_mts (adjust to actual service)
# Service: Cloud Speech-to-Text streaming (Alibaba Cloud)

# Set env vars before running:
# export ALIBABA_CLOUD_ACCESS_KEY_ID="your-id"
# export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-secret"


async def stream_chunks(source_async_iter):
    """Yield audio chunks from an async iterator and receive partial transcripts from Alibaba Cloud Speech API."""
    import alibabacloud_mts

    client = alibabacloud_mts.StreamingSpeechClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        region="cn-hangzhou",
    )
    async for chunk_bytes in source_async_iter:
        response = client.recognize_streaming(
            audio_chunk=chunk_bytes, config={"model": "general"}
        )
        yield response.get("partial_transcript", "")


# Example usage (run with an async generator that yields bytes)
# asyncio.run(stream_chunks(async_audio_provider()))
