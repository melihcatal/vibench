import os
from deepgram import sdk

# Local helper exposing Deepgram client creation with env var for API key

API_KEY = os.getenv("DEEPGRAM_API_KEY")


def get_client():
    """Create and return a reusable Deepgram Streaming client."""
    return sdk.StreamingClient(API_KEY)
