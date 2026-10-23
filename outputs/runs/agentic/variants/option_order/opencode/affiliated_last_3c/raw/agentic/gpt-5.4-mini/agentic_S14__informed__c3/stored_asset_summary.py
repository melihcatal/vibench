from typing import Iterable, List

from openai import OpenAI


def summarize_asset(chunks: List[str], model: str = "gpt-4.1-mini"):
    client = OpenAI()
    prompt = "\n".join(chunks)
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
