from openai import OpenAI


client = OpenAI()


def audit_summary(events: list[dict]) -> str:
    prompt = f"Summarize these federated login audit events concisely: {events}"
    result = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return result.choices[0].message.content or ""
