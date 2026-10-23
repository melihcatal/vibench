import asyncio
import aiohttp
import json
from speech_client import SpeechClient
from speech_models import SpeechModels

# Anthropic Messages API (service=Anthropic Messages API)
# SDK: anthropic
# Auth: ANTHROPIC_API_KEY

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("Environment variable ANTHROPIC_API_KEY not set")


async def summarize_meeting(stream_source):
    """
    Streams transcript chunks via SpeechClient, buffers them into meeting segments,
    and calls Anthropic to generate a concise summary.
    Yields (segment_id, summary) tuples.
    """
    client = SpeechClient("google")  # replace with actual provider if needed
    anthropic = anthropic.Client(ANTHROPIC_API_KEY)
    segment = []
    segment_id = 1
    async for chunk in client.stream_microphone():
        chunk_text = client._normalize_response(chunk)
        if chunk_text:
            segment.append(chunk_text)
            # Every 30 seconds (approx.) or when a pause longer than 2 seconds occurs
            # send current segment to Anthropic for summarization
            # Here we simulate a pause check with a simple counter
            if len(segment) >= 5:  # placeholder for timing logic
                full_text = " ".join(segment)
                response = await anthropic.completions.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=200,
                    temperature=0.0,
                    messages=[
                        {
                            "role": "user",
                            "text": f"Summarize this meeting transcript in 2-3 sentences:\n{full_text}",
                        }
                    ],
                )
                summary = response.completion
                yield segment_id, summary
                segment = []
                segment_id += 1


if __name__ == "__main__":

    async def demo():
        async for seg, summ in summarize_meeting(iter(["dummy"] * 6)):
            print(f"Segment {seg}: {summ}")

    asyncio.run(demo())
