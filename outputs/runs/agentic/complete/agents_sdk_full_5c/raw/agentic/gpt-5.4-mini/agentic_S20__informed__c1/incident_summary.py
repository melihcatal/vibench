from __future__ import annotations

from openai import OpenAI

from observability_models import coerce_events


def incident_summary(log_response: dict) -> str:
    client = OpenAI()
    events = coerce_events(log_response)
    prompt = "Summarize the incident impact, suspected root cause, and immediate next steps from these logs:\n"
    prompt += "\n".join(str(event) for event in events[:20])
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You produce concise incident-review summaries."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
