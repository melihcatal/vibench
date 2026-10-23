# [SAME-SCENARIO] stream_chunks.py
import asyncio

import speech_client as sc

# Provider: Google Cloud Speech-to-Text Streaming (imported from speech_client)

async def stream_audio_chunks(source_async_iterable, language_code="en-US", punctuation=True):
    """Stream audio chunks from an async iterable (e.g., network socket, file) to the recognizer.

    Args:
        source_async_iterable: an async generator yielding bytes (raw PCM).
        language_code: BCP-47 language identifier.
        punctuation: enable automatic punctuation.

    Yields:
        Partial and final recognition results.
    """
    async for result in sc.recognize_streaming(source_async_iterable,
                                               language_code=language_code,
                                               enable_automatic_punctuation=punctuation):
        yield result

# Example usage (uncomment for local testing):
# async def source():
#     with open("test.raw", "rb") as f:
#         while chunk := f.read(1024):
#             yield chunk
# async for r in stream_audio_chunks(source()):
#     print(r)
