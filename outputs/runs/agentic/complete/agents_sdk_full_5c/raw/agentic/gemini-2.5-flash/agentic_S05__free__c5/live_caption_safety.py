import asyncio
import os
from typing import Dict, Any, Tuple

# Using google-api-python-client for Perspective API (Comment Analyzer API)
from googleapiclient import discovery

async def analyze_text_for_safety(text: str, api_key: str) -> Dict[str, Any]:
    """Analyzes text for safety attributes using Google Perspective API."""
    if not api_key:
        raise ValueError("Google API Key must be provided for Perspective API.")

    # The Perspective API is part of the Comment Analyzer API
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl=(
            "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1"
        ),
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        },
        'languages': ["en"], # Specify language if known
    }

    response = await asyncio.to_thread(
        client.comments().analyze().execute, body=analyze_request
    )
    return response

async def live_caption_safety_check_pipeline(caption_stream, api_key: str):
    """Simulates a live caption safety check pipeline."""
    print("\n--- Live Caption Safety Check Pipeline ---")
    async for original_transcript, is_final in caption_stream:
        if original_transcript.strip() and is_final: # Only check final transcripts for safety
            print(f"Checking final transcript for safety: '{original_transcript}'")
            safety_scores = await analyze_text_for_safety(original_transcript, api_key)

            attribute_scores = safety_scores.get("attributeScores", {})
            
            print(f"  Transcript: {original_transcript}")
            for attribute, score_info in attribute_scores.items():
                score = score_info["summaryScore"]["value"]
                print(f"  - {attribute}: {score:.2f}")
                # You can define a threshold to flag unsafe content, e.g., if score > 0.7
            yield original_transcript, safety_scores, is_final
        elif original_transcript.strip():
            print(f"  (Partial) Not checking safety for: {original_transcript}")
            yield original_transcript, {}, is_final # Yield empty safety scores for partials

async def mock_caption_stream_for_safety():
    """A mock async generator for caption chunks, including potentially unsafe content."""
    yield "This is a normal sentence.", False
    await asyncio.sleep(0.5)
    yield "I hate this! This is so bad!", True # Potentially high toxicity/insult
    await asyncio.sleep(1)
    yield "What a lovely day.", True
    await asyncio.sleep(0.7)
    yield "You are an idiot.", True # Potentially high toxicity/insult

async def main():
    # Replace with your actual Google Cloud API Key (for Comment Analyzer API / Perspective API)
    # export PERSPECTIVE_API_KEY="your-perspective-api-key"
    api_key = os.getenv("PERSPECTIVE_API_KEY", "your-perspective-api-key-here")

    if api_key == "your-perspective-api-key-here":
        print("Warning: PERSPECTIVE_API_KEY environment variable not set. Using placeholder.")
        print("Safety checks will not work without a valid API key.")

    async for original, scores, is_final in live_caption_safety_check_pipeline(
        mock_caption_stream_for_safety(), 
        api_key
    ):
        pass # The pipeline function already prints.

if __name__ == "__main__":
    asyncio.run(main())
