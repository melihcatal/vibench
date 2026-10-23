import os
import asyncio
import requests
from speech_models import RecognitionResponse

PERSPECTIVE_ENDPOINT = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

async def check_safe_transcript(transcript: str) -> bool:
    """Calls Perspective API to detect toxicity. Returns True if safe."""
    headers = {
        'key': PERSPECTIVE_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        'comment': {'text': transcript},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
    if response.status_code != 200:
        print('Perspective API error:', response.status_code, response.text)
        return False
    scores = response.json().get('attributeScores', {}).get('TOXICITY', {})\n.get('summaryScore', {})
    score = scores.get('value', 0.0)
    # Threshold can be tuned; 0.5 is typical
    return score < 0.5

# Example usage within a streaming loop
# async for caption in caption_stream():
#     if await check_safe_transcript(caption):
#         print('Safe:', caption)
#     else:
#         print('Unsafe content detected')
