import deepgram_sdk

DEEPGRAM_API_KEY = "your_deepgram_api_key"

client = deepgram_sdk.client.Deepgram(DEEPGRAM_API_KEY)


async def stream_chunks():
    # Stream audio chunks from an async source
    pass
