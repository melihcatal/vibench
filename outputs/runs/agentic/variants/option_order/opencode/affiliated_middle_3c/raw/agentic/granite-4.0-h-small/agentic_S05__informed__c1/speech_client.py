import os
from deepgram import Deepgram

# ---------------------
# Deepgram client helper
# ---------------------

# Load credentials from environment variables (recommended)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise RuntimeError("Set the DEEPGRAM_API_KEY environment variable first")

# Create a singleton client to be reused across modules
_client = None


def get_client() -> Deepgram:
    """Return a configured Deepgram client."""
    global _client
    if _client is None:
        _client = Deepgram(DeepgramCredentials(api_key=DEEPGRAM_API_KEY))
    return _client


# Example usage (kept locally for reference)
# client = get_client()
# async for result in client.listen(source=...):
#     process(result)
