import os
from typing import List, Sequence

from openai import OpenAI


def batch_translate(texts: Sequence[str], source_language: str, target_language: str, model: str = "gpt-4.1-mini") -> List[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    f"Translate each input string from {source_language} to {target_language}. "
                    "Return a JSON array of translated strings in the same order, preserving order exactly."
                ),
            },
            {
                "role": "user",
                "content": "\n".join(f"{i}: {text}" for i, text in enumerate(texts)),
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    output_text = response.output_text
    data = __import__("json").loads(output_text)
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of translations")
    if len(data) != len(texts):
        raise ValueError("Translation count did not match input count")
    return [str(item) for item in data]
