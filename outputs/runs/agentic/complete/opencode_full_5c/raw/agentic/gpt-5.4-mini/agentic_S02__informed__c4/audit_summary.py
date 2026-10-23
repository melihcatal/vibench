import os
from typing import List

from openai import OpenAI


def summarize_audit_events(events: List[dict], model: str = "gpt-5.4-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = {"events": events}
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Summarize federated-login audit events briefly.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return response.choices[0].message.content or ""
