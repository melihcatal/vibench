import json
import asyncio
import sys
from typing import AsyncIterable

# Load configuration (API key) from helper file
from speech_client import load_config
config = load_config()
PERSPECTIVE_API_KEY = config["PERSPECTIVE_API_KEY"]

async def check_unsafe(captions: AsyncIterable[str]):
    """Iterate over caption chunks and flag those containing toxic content using Perspective API.""",
    import requests
    headers = {"key": PERSPECTIVE_API_KEY}
    for caption in captions:
        payload = {"comment": {"text": caption, "type": "PLAIN_TEXT"},
                   "languages": ["en"],
                   "requestedAttributes": {"TOXICITY": {}}}
        resp = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
                             headers=headers, json=payload).json()
        score = resp["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        if score > 0.8:
            print(f"[UNSAFE] {caption} (score {score})")
        else:
            print(f"[SAFE]   {caption} (score {score})")

if __name__ == "__main__":
    # Example: read lines from stdin as caption chunks
    async def caption_source():
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            yield line.strip()
    asyncio.run(check_unsafe(caption_source()))
