import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def build_messages(context: str, question: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Answer the user's question using only the provided context. If the context does not contain the answer, say you don't know.",
        },
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
    ]


def answer_with_context(context: str, question: str) -> str:
    api_key = os.environ["OPENAI_API_KEY"]
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": build_messages(context, question),
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: answer_with_context.py <context> <question>")
    context = sys.argv[1]
    question = sys.argv[2]
    print(answer_with_context(context, question))


if __name__ == "__main__":
    main()
