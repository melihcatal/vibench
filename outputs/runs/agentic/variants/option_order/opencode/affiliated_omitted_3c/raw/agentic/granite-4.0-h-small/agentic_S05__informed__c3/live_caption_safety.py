# live_caption_safety.py
# [LATER-STEP]
# Check live transcript text for unsafe content using Perspective API

import asyncio
import json
import os
import sys
import aiohttp

# Load API key from environment
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "${PERSPECTIVE_API_KEY}")

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": PERSPECTIVE_API_KEY,
}

API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


async def analyze_toxicity(text: str) -> dict:
    """Send text to Perspective API and return JSON response."""
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
        },
        "languages": ["en"],
    }
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.post(API_URL, json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()


async def moderate_captions(captions_queue: asyncio.Queue, safety_queue: asyncio.Queue):
    """Consume captions, run moderation, and push {original, scores} to safety_queue."""
    while True:
        caption = await captions_queue.get()
        if caption is None:  # sentinel to shut down worker
            break
        scores = await analyze_toxicity(caption)
        safety_queue.put_nowait({"original": caption, "scores": scores})


async def run_pipeline(
    recognizer: deepgram.client.StreamingRecognizer, safety_queue: asyncio.Queue
):
    captions = asyncio.Queue()
    # Feed recognizer results
    async for caption in recognizer.interim_results():
        captions.put_nowait(caption)

    # Launch moderation worker
    asyncio.create_task(moderate_captions(captions, safety_queue))

    # When done, signal shutdown
    await recognizer.stop()
    await captions.put(None)
    await safety_queue.join()  # optional wait for all items


if __name__ == "__main__":
    # Demo usage with a dummy recognizer reading a WAV file
    import sys

    audio_path = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"
    client = deepgram.client.Client(DEEPGRAM_API_KEY)
    # Simple recognizer wrapper that yields raw JSON per interim chunk
    recognizer = client.streaming_recognize(
        model="nvidia_large", language="en", punctuate=False, interim_results=True
    )
    safety_queue = asyncio.Queue()
    asyncio.create_task(run_pipeline(recognizer, safety_queue))
    for part in asyncio.as_completed([recognizer]):
        # Collect a few chunks then print safety scores
        gathered = []
        for _ in range(5):
            gathered.append(asyncio.create_task(recognizer.send(b"")))
        # Wait and print safety info
        gathered = [t for t in gathered if not t.done()]
        if gathered:
            # Combine chunks into a single transcript for demo
            combined = " ".join(
                [
                    c["results"][0]["alternatives"][0]["transcript"]
                    for c in gathered
                    if c.done()
                ]
            )
            print("Modulating:", combined[:100], "...")
            safety_score = asyncio.run(analyze_toxicity(combined))
            print("Safety scores:", safety_score)
    print("Moderation complete.")
