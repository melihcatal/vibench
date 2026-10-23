import os
from deepgram import DeepgramClient

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("DEEPGRAM_API_KEY environment variable is required.")

dg_client = DeepgramClient(DEEPGRAM_API_KEY)
