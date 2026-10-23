import os
from typing import List

from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_audit(events: List[str]) -> str:
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize federated-login audit events succinctly.",
            },
            {"role": "user", "content": "\n".join(events)},
        ],
    )
    return response.choices[0].message.content or ""
