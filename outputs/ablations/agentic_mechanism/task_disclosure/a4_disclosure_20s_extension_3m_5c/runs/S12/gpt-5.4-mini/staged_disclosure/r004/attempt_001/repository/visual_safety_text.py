import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _extract_text(payload: Dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str) and payload["output_text"].strip():
        return payload["output_text"].strip()
    output = payload.get("output", [])
    parts: List[str] = []
    for item in output:
        content = item.get("content", []) if isinstance(item, dict) else []
        for block in content:
            if isinstance(block, dict):
                text = block.get("text")
                if isinstance(text, str):
                    parts.append(text)
    return "\n".join(parts).strip()


def check_generated_visual_labels(labels: List[str]) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        "Review these generated visual labels for unsafe text. "
        "Return JSON with keys unsafe (boolean) and reasons (array of strings). Labels: "
        + ", ".join(labels)
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": prompt,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    text = _extract_text(payload)
    return {"provider": "openai", "model": OPENAI_MODEL, "result": text}


if __name__ == "__main__":
    import json
    import sys

    labels = sys.argv[1:]
    print(json.dumps(check_generated_visual_labels(labels)))
