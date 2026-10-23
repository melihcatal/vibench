import os

from openai import OpenAI


def moderation_summary(decisions, model: str = "gpt-4o-mini"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        "Summarize the moderation decisions concisely with risk highlights.\n"
        + str(decisions)
    )
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
