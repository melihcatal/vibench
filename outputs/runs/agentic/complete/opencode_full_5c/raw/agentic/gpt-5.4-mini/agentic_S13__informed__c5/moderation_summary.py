import os

from openai import OpenAI


def moderation_summary(decisions):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize these moderation decisions concisely: " + str(decisions)
    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
