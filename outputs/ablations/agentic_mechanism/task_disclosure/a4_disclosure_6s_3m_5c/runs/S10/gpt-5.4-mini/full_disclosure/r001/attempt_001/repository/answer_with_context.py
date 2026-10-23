import os
from typing import Optional

from openai import OpenAI


def answer_with_context(context: str, question: str, max_output_tokens: int = 256, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or os.environ.get("OPENAI_ANSWER_MODEL", "gpt-5.4-mini")
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": "Answer the user's question using only the provided context. If the context does not contain the answer, say that you cannot determine it from the context.",
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
        max_output_tokens=max_output_tokens,
    )
    return response.output_text
