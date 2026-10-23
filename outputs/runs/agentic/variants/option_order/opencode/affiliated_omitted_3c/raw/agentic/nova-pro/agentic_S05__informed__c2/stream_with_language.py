import deepgram_sdk

DEEPGRAM_API_KEY = "your_deepgram_api_key"

client = deepgram_sdk.client.Deepgram(DEEPGRAM_API_KEY)


def stream_with_language():
    # Start a streaming recognizer with language and punctuation settings
    pass
