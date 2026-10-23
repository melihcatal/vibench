from openai import OpenAI


def moderation_summary(decisions, model="gpt-4.1-mini"):
    client = OpenAI()
    prompt = f"Summarize these moderation decisions concisely: {decisions}"
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
