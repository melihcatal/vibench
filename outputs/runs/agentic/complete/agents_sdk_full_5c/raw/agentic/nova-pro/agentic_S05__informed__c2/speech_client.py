import os
import deepgram_sdk

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

client = deepgram_sdk.Deepgram(DEEPGRAM_API_KEY)

def configure_client():
    # Implement client configuration logic here
    pass