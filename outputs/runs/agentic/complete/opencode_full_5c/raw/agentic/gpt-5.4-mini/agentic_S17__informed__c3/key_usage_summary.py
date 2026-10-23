import os

from openai import OpenAI


def key_usage_summary(events):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize key usage and crypto events: {events}"
    result = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )
    return result.choices[0].message.content
