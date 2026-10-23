import os
from deepgram import DeepgramClient


def get_dg_client(api_key: str | None = None) -> DeepgramClient:
    if api_key is None:
        api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is required.")
    return DeepgramClient(api_key)
