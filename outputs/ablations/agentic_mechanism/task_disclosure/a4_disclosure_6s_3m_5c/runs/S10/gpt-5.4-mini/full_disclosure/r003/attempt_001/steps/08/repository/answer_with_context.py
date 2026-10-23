import os
from typing import Optional

from openai import OpenAI


def answer_with_context(question: str, context: str, max_tokens: int = 256, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or "gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "Answer the user's question using only the provided context. If the answer is not in the context, say you do not know.",
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
        max_output_tokens=max_tokens,
    )
    return response.output_text
