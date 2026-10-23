import asyncio
import os
import requests
import json


async def check_caption_safety(text: str):
    """
    Checks live transcript text for unsafe content using Perspective API.
    """
    PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
    if not PERSPECTIVE_API_KEY:
        print(
            "WARNING: PERSPECTIVE_API_KEY environment variable not set. Content safety check will be skipped."
        )
        return {"summary": "Content safety check skipped due to missing API key."}

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    try:
        response = await asyncio.to_thread(
            requests.post, url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
        analysis_result = response.json()
        return analysis_result
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety with Perspective API: {e}")
        return {"error": str(e)}


async def live_caption_safety(caption_stream_async_generator):
    """
    Checks live captions from an async generator for unsafe content.
    """
    async for caption_event in caption_stream_async_generator:
        if caption_event["is_final"]:
            safety_check_result = await check_caption_safety(
                caption_event["transcript"]
            )
            yield {
                "original_text": caption_event["transcript"],
                "safety_analysis": safety_check_result,
            }
        else:
            # For partial results, we might not want to perform a full safety check
            yield {
                "original_text": caption_event["transcript"],
                "safety_analysis": "Partial transcript - no full analysis",
            }


if __name__ == "__main__":

    async def dummy_caption_source():
        # Simulate a stream of transcription results
        await asyncio.sleep(1)
        yield {"transcript": "That was a terrible thing to say!", "is_final": False}
        await asyncio.sleep(1)
        yield {
            "transcript": "That was a terrible thing to say! You are very bad.",
            "is_final": True,
        }
        await asyncio.sleep(1)
        yield {"transcript": "This is a normal conversation.", "is_final": True}

    async def main():
        # Set a dummy API key for testing purposes if not already set
        os.environ["PERSPECTIVE_API_KEY"] = os.environ.get(
            "PERSPECTIVE_API_KEY", "YOUR_PERSPECTIVE_API_KEY_HERE"
        )
        print("Starting live caption safety check...")
        try:
            async for result in live_caption_safety(dummy_caption_source()):
                print(f"Original: {result['original_text']}")
                print(
                    f"Safety Analysis: {json.dumps(result['safety_analysis'], indent=2)}"
                )
        except KeyboardInterrupt:
            print("\nStopped live caption safety check.")

    asyncio.run(main())
