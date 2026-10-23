import json
from deepgram import Deepgram


# Scoring utility to evaluate partial and final transcript results
async def evaluate_transcript(result, threshold=0.8):
    text = result.get("transcript", "")
    confidence = result.get("confidence", 0)
    # Yield a decision based on confidence or (for final) length
    if result["is_final"]:
        is_acceptable = confidence >= threshold or len(text) > 0
    else:
        is_acceptable = confidence >= threshold
    return {"text": text, "is_acceptable": is_acceptable}


async def main():
    DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"
    client = Deepgram(DeepgramCredentials(api_key=DEEPGRAM_API_KEY))

    # Mock a streaming response iterable
    async def streaming_response():
        # Simulate two interim chunks then a final chunk
        for _ in range(2):
            yield {"partial": "Hello ", "confidence": 0.75, "is_final": False}
        yield {"transcript": "Hello world!", "confidence": 0.92, "is_final": True}

    async for result in streaming_response():
        scored = await evaluate_transcript(result)
        print(json.dumps(scored))


if __name__ == "__main__":
    asyncio.run(main())
