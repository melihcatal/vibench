import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def answer_with_context(question: str, context: str, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_id = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "Answer the question using only the provided context. If the context does not contain the answer, say you don't know."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
    ]
    response: Any = client.chat.completions.create(
        model=model_id,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content or ""
