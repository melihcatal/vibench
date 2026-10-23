# SAME-SCENARIO: partial_results.py
# handles partial and final streaming recognition events
import asyncio
import deepgram  # pip install deepgram-sdk-python

# Deepgram Streaming SDK imported – provider identifiable
DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"


async def handle_streaming_events(url: str = "wss://api.deepgram.io/v1/stream"):
    """Connect to Deepgram streaming endpoint and process interim + final events.

    Yields:
        dict: Each event payload containing "transcript", "is_final", etc.
    """
    async with deepgram.Stream(url, DEEPGRAM_API_KEY) as ws:
        # Send initial configuration (use Nova model for demo)
        config = {
            "model": "nova",
            "language": "en",
            "punctuation": True,
            "interim_results": True,
        }
        await ws.send_json({"config": config})

        while True:
            message = await ws.receive_json()
            # Deepgram streaming messages carry an "is_final" flag
            is_final = message.get("is_final", False)
            alternatives = message.get("alternatives", [])
            transcript = alternatives[0].get("transcript", "") if alternatives else ""
            print(
                f"{('Final' if is_final else 'Interim')}: {transcript}{' (final)' if is_final else ''}"
            )
            yield {"transcript": transcript, "is_final": is_final}


if __name__ == "__main__":
    asyncio.run(handle_streaming_events())
