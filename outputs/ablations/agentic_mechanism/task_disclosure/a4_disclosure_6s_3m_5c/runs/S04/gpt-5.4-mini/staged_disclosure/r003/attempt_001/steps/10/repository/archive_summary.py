import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def load_input() -> Dict[str, Any]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            return json.load(f)
    data = sys.stdin.read().strip()
    if not data:
        return {}
    return json.loads(data)


def build_prompt(payload: Dict[str, Any]) -> str:
    transcript = payload.get("transcript", "")
    results = payload.get("transcription_results", payload.get("results", []))
    if isinstance(results, list):
        results_text = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        results_text = str(results)
    return (
        "Summarize the transcription results concisely. "
        "Focus on key topics, notable entities, action items, and any uncertainties.\n\n"
        f"Transcript:\n{transcript}\n\n"
        f"Transcription results:\n{results_text}"
    )


def summarize_with_openai(prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You summarize transcription output."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    payload = load_input()
    prompt = build_prompt(payload)
    summary = summarize_with_openai(prompt)
    sys.stdout.write(summary)


if __name__ == "__main__":
    main()
