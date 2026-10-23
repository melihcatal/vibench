from __future__ import annotations

import os
from typing import Any, Dict

import httpx


OPENAI_MODERATIONS_URL = "https://api.openai.com/v1/moderations"


async def check_live_caption_safety(text: str) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {"model": "omni-moderation-latest", "input": text}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            OPENAI_MODERATIONS_URL, json=payload, headers=headers
        )
        response.raise_for_status()
        body = response.json()
    result = body["results"][0]
    return {
        "provider": "openai",
        "flagged": result["flagged"],
        "categories": result["categories"],
        "category_scores": result["category_scores"],
    }
