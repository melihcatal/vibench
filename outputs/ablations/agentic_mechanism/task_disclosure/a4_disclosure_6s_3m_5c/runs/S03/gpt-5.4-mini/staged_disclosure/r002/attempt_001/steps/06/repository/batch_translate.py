import os
from typing import List

from openai import OpenAI


def batch_translate(strings: List[str], target_language: str) -> List[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not strings:
        return []
    prompt = (
        "Translate each item into "
        f"{target_language}. Preserve the original order. "
        "Return only a JSON array of translated strings. "
        "Input strings: "
        f"{strings}"
    )
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    text = response.output_text.strip()
    import json

    result = json.loads(text)
    if not isinstance(result, list) or len(result) != len(strings):
        raise ValueError("Unexpected translation response")
    return [str(item) for item in result]
