# moderate_transcript.py (updated to embed utility import directly)
import os
import json
import boto3
import requests
import hashlib
from typing import Dict

# Azure AI Content Safety request data structure
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')
if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
    raise RuntimeError('Azure Content Safety credentials not configured')

def moderate_transcript(text: str) -> Dict:
    """Run content moderation on transcript text using Azure AI Content Safety."""
    payload = {
        "content": {
            "content": text,
            "locale": "en"
        }
    }
    response = requests.post(
        AZURE_CONTENT_SAFETY_ENDPOINT + "/contentsafety/text/analyze?api-version=2023-04-30",
        headers={
            "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
            "Content-Type": "application/json"
        },
        json=payload
    )
    return response.json()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: moderate_transcript.py <transcript_text>", file=sys.stderr)
        sys.exit(1)
    result = moderate_transcript(sys.argv[1])
    print(json.dumps(result, indent=2))
