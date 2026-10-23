import os
from typing import Optional

from openai import OpenAI


def summarize_asset(
    text: str, model: str = "gpt-5.4-mini", instruction: Optional[str] = None
) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = instruction or "Summarize the following asset content concisely."
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
