from openai import OpenAI


def audit_summary(events: list[str]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize federated-login audit events concisely.",
            },
            {"role": "user", "content": "\n".join(events)},
        ],
    )
    return response.choices[0].message.content or ""
