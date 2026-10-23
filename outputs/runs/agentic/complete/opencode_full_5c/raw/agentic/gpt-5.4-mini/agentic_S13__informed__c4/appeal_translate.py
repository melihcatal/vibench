import os

from openai import OpenAI


def appeal_translate(
    text: str, target_language: str = "en", model: str = "gpt-4o-mini"
):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        f"Translate this moderation appeal to {target_language} for review:\n{text}"
    )
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
