import deepgram_sdk

DEEPGRAM_API_KEY = "your_deepgram_api_key"

client = deepgram_sdk.client.Deepgram(DEEPGRAM_API_KEY)


def stream_microphone():
    # Stream microphone audio and yield interim transcripts
    pass
