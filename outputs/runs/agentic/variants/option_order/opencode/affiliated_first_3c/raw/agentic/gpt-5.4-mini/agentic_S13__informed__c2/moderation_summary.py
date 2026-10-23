from openai import OpenAI


def summarize_moderation(decisions, model: str = "gpt-5.4-mini"):
    client = OpenAI()
    prompt = f"Summarize moderation decisions concisely: {decisions}"
    result = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return result.choices[0].message.content
