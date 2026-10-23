from openai import OpenAI


def summarize_audit_events(events: list[dict]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize federated-login audit events concisely.",
            },
            {"role": "user", "content": str(events)},
        ],
    )
    return response.choices[0].message.content or ""
