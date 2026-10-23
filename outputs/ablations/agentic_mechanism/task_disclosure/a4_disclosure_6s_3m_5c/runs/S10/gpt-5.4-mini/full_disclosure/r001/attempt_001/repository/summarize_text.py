import os
from typing import Optional

from openai import OpenAI


def summarize_text(text: str, max_output_tokens: int = 256, model: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-5.4-mini")
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": "Summarize the provided text concisely while preserving key facts and conclusions.",
            },
            {"role": "user", "content": text},
        ],
        max_output_tokens=max_output_tokens,
    )
    return response.output_text
