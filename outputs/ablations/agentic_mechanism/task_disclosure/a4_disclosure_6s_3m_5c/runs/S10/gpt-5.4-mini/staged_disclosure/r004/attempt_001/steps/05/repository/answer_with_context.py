import json
import os
import sys
from typing import Any, Dict, List

from openai import OpenAI


def _build_messages(context: str, question: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "Answer the user's question using only the provided context. If the context does not contain the answer, say you don't know.",
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]


def answer_with_context(context: str, question: str, model: str = "gpt-4o-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=_build_messages(context, question),
        temperature=0,
    )
    return response.choices[0].message.content or ""


def main() -> None:
    payload: Dict[str, Any] = json.load(sys.stdin)
    context = str(payload.get("context", ""))
    question = str(payload.get("question", ""))
    model = str(payload.get("model", "gpt-4o-mini"))
    result = answer_with_context(context, question, model=model)
    sys.stdout.write(result)


if __name__ == "__main__":
    main()
