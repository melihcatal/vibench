import json

from openai import OpenAI


def summarize_audit(events: list[dict]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize federated login audit events."},
            {"role": "user", "content": json.dumps(events)},
        ],
    )
    return response.choices[0].message.content or ""
