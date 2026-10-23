import os
from deepgram import AsyncDeepgramClient


def get_async_stt_client() -> AsyncDeepgramClient:
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is required")
    return AsyncDeepgramClient(api_key=api_key)
