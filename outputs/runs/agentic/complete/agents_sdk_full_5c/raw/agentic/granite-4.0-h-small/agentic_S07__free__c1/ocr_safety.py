import os
from typing import List
from dotenv import load_dotenv
import httpx
from document_models import UnsafeContentCheckRequest, UnsafeContentCheckResponse

load_dotenv()
SAFETY_API_URL = os.getenv('SAFETY_API_URL', 'https://api.contentmoderation.com/v1')
SAFETY_API_KEY = os.getenv('SAFETY_API_KEY')

async def check_safety(text: str) -> UnsafeContentCheckResponse:
    """Check extracted document text for unsafe content using Perspective API."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SAFETY_API_URL}/comments:analyze",
            json=[{"text": text}],
            headers={"apikey": SAFETY_API_KEY},
        )
        resp.raise_for_status()
        results = resp.json()['results']
        # Return a simple boolean flag for demo
        unsafe = any(item['score'] > 0.8 for item in results)
        return UnsafeContentCheckResponse(is_unsafe=unsafe)
