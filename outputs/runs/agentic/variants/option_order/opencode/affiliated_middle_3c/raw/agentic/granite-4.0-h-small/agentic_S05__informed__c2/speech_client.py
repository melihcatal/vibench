import os
import deepgram  # Example client library

# Configuration loading helper
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise RuntimeError("Set DEEPGRAM_API_KEY environment variable")


def create_client():
    """Creates and returns a configured Deepgram Streaming client.
    Returns:
        deepgram.StreamingClient: ready-to-use client instance
    """
    return deepgram.StreamingClient(DEEPGRAM_API_KEY)


# Example usage in other modules:
# client = create_client()
# async with client.start_language('en-US') as s:
#     ...
