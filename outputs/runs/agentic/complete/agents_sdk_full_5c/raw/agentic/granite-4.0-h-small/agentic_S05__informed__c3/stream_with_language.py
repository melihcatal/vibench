import asyncio
import json
from dotenv import load_dotenv
import speech_client as sc

load_dotenv()

async def stream_with_language(language_code='en-US', enable_automatic_punctuation=True):
    """Start a streaming recognizer with language and punctuation configuration."""
    # Provider-specific configuration payload (example using Google Speech)
    config = {
        'config': {
            'language_code': language_code,
            'enable_automatic_punctuation': enable_automatic_punctuation,
            'speech_contexts': [{'phrases': ['weather']}],
            # Additional fields like encoding, sample_rate_hertz can go here
        }
    }
    # Start streaming request using helper utility
    await sc.start_streaming(config)
    # In a real app, capture audio and forward chunks to the same stream
    # Placeholder loop to keep the stream open
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(stream_with_language())
