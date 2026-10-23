from typing import List

from openai import OpenAI


def meeting_summary(chunks: List[str]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": "\n".join(chunks)}]
    )
    return response.choices[0].message.content or ""
