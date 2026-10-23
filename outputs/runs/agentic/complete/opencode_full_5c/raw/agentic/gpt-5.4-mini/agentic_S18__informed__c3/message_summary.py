from typing import Iterable, List

from openai import OpenAI


def summarize_messages(messages: List[str]) -> str:
    client = OpenAI()
    prompt = "Summarize these message processing results:\n" + "\n".join(messages)
    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""
