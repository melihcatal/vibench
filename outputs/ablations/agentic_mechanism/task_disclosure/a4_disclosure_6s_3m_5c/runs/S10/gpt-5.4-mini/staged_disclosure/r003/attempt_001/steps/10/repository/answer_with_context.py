import os
from typing import Optional

from openai import OpenAI


def answer_with_context(question: str, context: str, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    selected_model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    response = client.responses.create(
        model=selected_model,
        input=[
            {
                "role": "system",
                "content": "Answer the question using only the provided context. If the context does not contain the answer, say you don't know.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )
    return response.output_text


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("Usage: python answer_with_context.py <question> <context>")
    print(answer_with_context(sys.argv[1], sys.argv[2]))
