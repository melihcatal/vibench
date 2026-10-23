import os
from typing import Optional

from openai import OpenAI


def summarize_text(text: str, max_tokens: int = 256, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model or "gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize the provided text concisely and accurately.",
            },
            {"role": "user", "content": text},
        ],
        max_output_tokens=max_tokens,
    )
    return response.output_text
