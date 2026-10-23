import json
import os
import sys
from typing import List

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def summarize_meeting_chunks(chunks: List[str]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    if not chunks:
        raise ValueError("At least one transcript chunk is required")

    prompt = (
        "Summarize the live meeting transcript chunks into a concise meeting summary. "
        "Combine repeated ideas, preserve decisions, action items, blockers, and open questions. "
        "Return only the summary text.\n\n"
        + "\n\n".join(f"Chunk {index + 1}: {chunk}" for index, chunk in enumerate(chunks))
    )

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": "You summarize live meeting transcripts."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            }
        ),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> int:
    chunks = [line.rstrip("\n") for line in sys.stdin if line.strip()]
    print(summarize_meeting_chunks(chunks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
