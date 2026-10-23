# speech_client.py
# [HELPER]
# Local configuration and client helper utilities for Streaming Speech-to-Text with Deepgram

import os
import deepgram

# Load Deepgram API key from environment; you can set DEEPGRAM_API_KEY before running
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "${DEEPGRAM_API_KEY}")

# Create a reusable Deepgram client instance
client = deepgram.client.Client(DEEPGRAM_API_KEY)


# Helper to build a streaming recognizer with common defaults
async def build_streaming_recognizer(
    model: str = "nvidia_large",
    language: str = "en",
    punctuate: bool = False,
    interim_results: bool = False,
):
    """Assemble and return a Deepgram streaming recognizer with chosen parameters."""
    recognizer = client.streaming_recognize(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
    )
    return recognizer


# Example usage (can be called from any same-scenario file)
if __name__ == "__main__":
    import asyncio

    recognizer = asyncio.run(build_streaming_recognizer())
    print(
        "Built recognizer with model", recognizer.model, "language", recognizer.language
    )

# Provide the client for other modules to import
__all__ = ["client"]
