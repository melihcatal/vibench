import os
from deepgram import DeepgramClient, DeepgramClientOptions
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


def get_deepgram_client() -> DeepgramClient:
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")

    config = DeepgramClientOptions(
        verbose=0,  # Set to 1 for more verbose logging
    )

    # The DEEPGRAM_API_KEY is read from the environment variables by default.
    # You can also pass it directly to the client.
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY, config=config)
    return client
