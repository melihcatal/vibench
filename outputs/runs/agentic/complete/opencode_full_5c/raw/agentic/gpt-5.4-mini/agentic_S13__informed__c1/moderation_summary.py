from openai import OpenAI


def moderation_summary(decisions: list[dict]) -> str:
    client = OpenAI()
    prompt = (
        f"Summarize these moderation decisions for an operations reviewer: {decisions}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""
