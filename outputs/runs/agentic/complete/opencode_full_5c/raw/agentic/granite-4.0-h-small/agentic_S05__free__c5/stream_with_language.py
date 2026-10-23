# [SAME-SCENARIO] stream_with_language.py
# Starts a streaming recognizer with language and punctuation settings using OpenAI Whisper ASR (hosted)
import asyncio
from openai import OpenAI

# Provider identifier
PROVIDER = "openai"

client = OpenAI()


async def stream_with_language(audio_stream, language="en", punctuation=True):
    """Stream audio to OpenAI Whisper streaming endpoint with language and punctuation options."""
    # Whisper streaming endpoint (hosted API)
    response = client.audio.transcriptions(
        model="whisper-1",
        language=language,
        punctuate=punctuation,
        # The API expects the entire audio file, but we can stream chunks via async iteration
        # Placeholder for actual streaming implementation
        # This snippet shows the configuration; replace with real streaming transport
    )
    # Simulate receiving partial transcripts
    for chunk in response.stream():
        # Whisper streaming returns JSON lines with partial results
        text = chunk.get("text", "")
        is_final = False  # Final result returned in last chunk
        yield {
            "provider": PROVIDER,
            "transcript": text,
            "is_final": is_final,
        }


# Example usage (uncomment to run)
# async def main():
#     # audio_stream would be an async iterator of audio chunks
#     async for result in stream_with_language(audio_stream=True, language="en"):
#         print(result)
# asyncio.run(main())
