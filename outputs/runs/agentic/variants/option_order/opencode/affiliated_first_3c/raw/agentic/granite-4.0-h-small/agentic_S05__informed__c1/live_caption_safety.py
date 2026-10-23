"""
Check live transcript chunks for unsafe content using watsonx guardrails.
Guardrails endpoint: https://api.watsonx.ai/ai-runtime/v1/guardrails
Credentials: WATSONX_API_KEY, WATSONX_PROJECT_ID
Requires watsonx-ai SDK (ibm-watsonx-ai).
"""

import os
import asyncio
import requests
from typing import Iterator

GUARDRAILS_ENDPOINT = "https://api.watsonx.ai/ai-runtime/v1/guardrails"


def check_toxicity(text: str) -> bool:
    """
    Calls watsonx guardrails detection API for toxicity.
    Returns True if toxic, False otherwise.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": [{"text": text}],
        "model": "viola",  # default toxicity model
    }
    try:
        resp = requests.post(
            GUARDRAILS_ENDPOINT, headers=headers, json=payload, timeout=10
        )
        if resp.status_code != 200:
            raise RuntimeError(f"Guardrails API error: {resp.status_code}")
        result = resp.json()
        # Simple heuristic: if any unsafe category detected, consider toxic
        unsafe = result.get("outputs", [{}])[0].get("unsafe", [])
        return bool(unsafe)
    except Exception as e:
        print("Guardrails API failure:", e)
        return False  # fallback safe


async def safety_filter(source: Iterator[str]) -> Iterator[str]:
    """Yields only safe transcript chunks."""
    for chunk in source:
        if not check_toxicity(chunk):
            yield chunk
        else:
            print("Unsafe content detected; omitted:")
            print(chunk)


if __name__ == "__main__":
    # Demo with a simple list of caption chunks
    captions = [
        "Everything is fine. This is a good meeting.",
        "This content is toxic and should be filtered out.",
    ]
    safe = safety_filter(captions)
    for s in safe:
        print("Safe chunk:", s)
