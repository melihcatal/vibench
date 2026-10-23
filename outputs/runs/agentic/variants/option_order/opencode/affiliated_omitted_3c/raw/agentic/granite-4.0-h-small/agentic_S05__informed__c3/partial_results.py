# partial_results.py
# [SAME-SCENARIO]
# Handles partial and final streaming recognition events from Deepgram

import asyncio
import deepgram

# Deepgram authentication
DEEPGRAM_API_KEY = "${DEEPGRAM_API_KEY}"


async def handle_partial_results(recognizer):
    """Consume partial results as they arrive from Deepgram streaming recognizer."""
    async for partial in recognizer.partial_results():
        # partial is a dict containing interim transcript info
        interim = (
            partial.get("results", [{}])[0]
            .get("alternatives", [{}])[0]
            .get("transcript", "")
        )
        print("Partial result:", interim)


async def handle_final_results(recognizer):
    """Consume final recognition result once the stream ends."""
    result = await recognizer.final_result()
    if result:
        final = (
            result.get("results", [{}])[0]
            .get("alternatives", [{}])[0]
            .get("transcript", "")
        )
        print("Final transcript:", final)


async def run_with_partial_handling():
    client = deepgram.client.Client(DEEPGRAM_API_KEY)
    # Create a recognizer with interim support
    recognizer = client.streaming_recognize(
        model="nvidia_large", language="en", punctuate=False, interim_results=True
    )
    # Run partial handling in background
    partial_task = asyncio.create_task(handle_partial_results(recognizer))
    # Simulate sending audio (using a dummy byte stream for demo)
    async for _ in range(5):
        await recognizer.send(b"dummy audio data")
        await asyncio.sleep(0.2)
    # Close the stream to trigger final result
    await recognizer.close()
    await partial_task
    await handle_final_results(recognizer)


if __name__ == "__main__":
    asyncio.run(run_with_partial_handling())
