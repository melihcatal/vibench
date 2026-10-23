import os
from typing import List

from openai import OpenAI


def check_unsafe_copy(text: str, *, model: str = "gpt-4.1-mini") -> List[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "Detect unsafe localized copy. Return a concise list of issues."},
            {"role": "user", "content": text},
        ],
    )
    output = getattr(response, "output_text", None) or str(response)
    return [line.strip("- •\t ") for line in output.splitlines() if line.strip()]
