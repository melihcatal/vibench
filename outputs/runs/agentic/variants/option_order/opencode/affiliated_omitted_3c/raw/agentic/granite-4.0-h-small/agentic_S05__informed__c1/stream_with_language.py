# SAME-SCENARIO: stream_with_language.py
# starts a streaming recognizer with language and punctuation settings
import asyncio
import deepgram  # pip install deepgram-sdk-python

# Deepgram Streaming SDK imported – provider identifiable
DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"


async def stream_with_specific_language(language: str = "es", punctuation: bool = True):
    """Open a streaming WebSocket to Deepgram with language and punctuation config.

    Args:
        language: ISO 639‑1 language code (e.g., 'es' for Spanish).
        punctuation: Whether to enable punctuation in the transcription.
    """
    url = "wss://api.deepgram.io/v1/stream"
    async with deepgram.Stream(url, DEEPGRAM_API_KEY) as ws:
        init_payload = {
            "config": {
                "model": "nova",
                "language": language,
                "punctuation": punctuation,
                "interim_results": True,
            }
        }
        await ws.send_json(init_payload)

        # Continuously read audio from microphone (placeholder)
        while True:
            # In a real implementation you would read from a microphone here
            # For demo, we just echo back a tiny silent chunk to keep connection alive
            await asyncio.sleep(0.5)


if __name__ == "__main__":
    # Example: Spanish with punctuation enabled
    asyncio.run(stream_with_specific_language())
