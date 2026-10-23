from __future__ import annotations

import os
from typing import Iterable

import httpx


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


async def summarize_meeting_chunks(chunks: Iterable[str]) -> str:
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk.strip())
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize the meeting transcript into decisions, action items, and risks.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": transcript}],
            },
        ],
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            OPENAI_RESPONSES_URL, json=payload, headers=headers
        )
        response.raise_for_status()
        body = response.json()
    return body["output"][0]["content"][0]["text"]
