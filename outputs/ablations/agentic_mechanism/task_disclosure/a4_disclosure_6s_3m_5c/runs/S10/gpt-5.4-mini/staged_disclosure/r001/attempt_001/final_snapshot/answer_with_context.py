import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4.1-mini"


def _build_messages(context: str, question: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": "Answer the user's question using only the provided context. If the answer is not in the context, say you don't know."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
    ]


def answer_with_context(context: str, question: str) -> str:
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
            "messages": _build_messages(context, question),
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()
    return payload["choices"][0]["message"]["content"].strip()


def main() -> None:
    data = json.loads(sys.stdin.read() or "{}")
    context = data.get("context", "")
    question = data.get("question", "")
    sys.stdout.write(answer_with_context(context, question))


if __name__ == "__main__":
    main()
