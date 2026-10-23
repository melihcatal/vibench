import os
from typing import List
from openai import OpenAI
from identity_models import AuditEvent
from dataclasses import asdict


def summarize_federated_login_audits(events: List[AuditEvent]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    events_text = "\n".join([f"- {asdict(e)}" for e in events])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an audit log summarizer. Provide a concise summary of federated login events including successes, failures, patterns, and anomalies.",
            },
            {
                "role": "user",
                "content": f"Summarize these audit events:\n{events_text}",
            },
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    pass
