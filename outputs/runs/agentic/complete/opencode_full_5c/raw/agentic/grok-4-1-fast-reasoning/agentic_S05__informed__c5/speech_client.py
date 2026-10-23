import os
from deepgram import DeepgramClient

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
