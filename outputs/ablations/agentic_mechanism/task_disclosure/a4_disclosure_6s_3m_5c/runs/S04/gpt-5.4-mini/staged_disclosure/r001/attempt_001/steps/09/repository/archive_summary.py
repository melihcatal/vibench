import os
import json
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def summarize_transcription(transcription_result: Dict[str, Any]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    transcript = transcription_result.get("transcript") or transcription_result.get("text") or ""
    metadata = transcription_result.get("metadata") or {}

    prompt = {
        "task": "Summarize transcription results",
        "transcript": transcript,
        "metadata": metadata,
        "instructions": [
            "Produce a concise summary of the transcription.",
            "Include key topics, notable entities, and action items if present.",
            "Keep output brief and directly useful.",
        ],
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You summarize transcription results."},
                {"role": "user", "content": json.dumps(prompt)},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    raise SystemExit("Import summarize_transcription(transcription_result) to use this module.")
